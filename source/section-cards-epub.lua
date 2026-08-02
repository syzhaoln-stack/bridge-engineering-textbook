-- EPUB fallback for section flashcards.
-- HTML offers a full practice deck; a linear EPUB keeps only each H2's first,
-- author-reviewed core card so the book does not become a 251-card catalogue.

if not FORMAT:match("epub") then
  return {}
end

local ok, DATA = pcall(dofile, "interactive/section-card-data.lua")
if not ok then
  error("Unable to load interactive/section-card-data.lua: " .. tostring(DATA))
end

local function normalize_heading(value)
  return tostring(value or "")
    :gsub("“", '"')
    :gsub("”", '"')
    :gsub("‘", "'")
    :gsub("’", "'")
end

local NORMALIZED_DATA = {}
for heading, cards in pairs(DATA) do
  NORMALIZED_DATA[normalize_heading(heading)] = cards
end

local function inline_text(value)
  return pandoc.Str(tostring(value or ""))
end

local function field(label, value)
  if type(value) == "table" then
    value = table.concat(value, "；")
  end
  return pandoc.Para({ pandoc.Strong({ inline_text(label .. "：") }), inline_text(value) })
end

local function clean(value)
  return tostring(value or ""):gsub("%s+", " "):gsub("^%s+", ""):gsub("%s+$", "")
end

local function utf8_characters(value)
  local result = {}
  for _, codepoint in utf8.codes(clean(value)) do
    table.insert(result, utf8.char(codepoint))
  end
  return result
end

local function utf8_length(value)
  return #utf8_characters(value)
end

local function trim_text(value, maximum, minimum_break)
  local chars = utf8_characters(value)
  if #chars <= maximum then
    return table.concat(chars)
  end

  local preferred = { ["。"] = true, ["！"] = true, ["？"] = true, ["；"] = true }
  local cut = nil
  for index = maximum, minimum_break, -1 do
    if preferred[chars[index]] then
      cut = index
      break
    end
  end
  if not cut then
    for index = maximum - 1, minimum_break, -1 do
      if chars[index] == "，" then
        cut = index
        break
      end
    end
  end

  local end_at = cut or (maximum - 1)
  local result = table.concat(chars, "", 1, end_at):gsub("[，；%s]+$", "")
  if not cut then
    result = result .. "…"
  end
  return result
end

local function short_answer(card)
  local idea = clean(card.idea)
  if utf8_length(idea) >= 35 then
    return trim_text(idea, 90, 35)
  end
  return trim_text(idea .. " " .. clean(card.mechanism), 90, 35)
end

function Header(header)
  if header.level ~= 2 then
    return nil
  end

  local heading = normalize_heading(pandoc.utils.stringify(header.content))
  local cards = NORMALIZED_DATA[heading]
  if not cards or not cards[1] then
    return nil
  end

  local card = cards[1]
  local answer = short_answer(card)
  local mechanism = clean(card.mechanism)
  local card_blocks = {
    pandoc.Para({
      pandoc.Emph({ inline_text("这一节先想一下　" .. tostring(card.concept or card.theme or "")) })
    }),
    pandoc.Para({ pandoc.Strong({ inline_text(card.question or "") }) }),
    field("短答", answer)
  }

  -- If the short answer had to stop before the full mechanism, retain the
  -- mechanism once.  If it is already wholly present, do not repeat it.
  if mechanism ~= "" and not answer:find(mechanism, 1, true) then
    table.insert(card_blocks, field("为什么", mechanism))
  end
  local card_block = pandoc.Div(
    card_blocks,
    pandoc.Attr("", { "section-flashcard", "section-flashcard--epub" })
  )
  local group = pandoc.Div(
    { card_block },
    pandoc.Attr("", { "section-flashcards", "section-flashcards--epub" })
  )
  return { header, group }
end
