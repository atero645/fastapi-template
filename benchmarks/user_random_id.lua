-- random_id.lua
request = function()
    local user_id = math.random(1, 100)
    path = "/users/" .. user_id
    return wrk.format("GET", path)
end