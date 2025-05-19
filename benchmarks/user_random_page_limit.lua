-- random_page_limit.lua
request = function()
    local limit = math.random(10, 25)
    local page = math.random(1, 20)
    local path = string.format("/users/?page=%d&limit=%d", page, limit)
    return wrk.format("GET", path)
end