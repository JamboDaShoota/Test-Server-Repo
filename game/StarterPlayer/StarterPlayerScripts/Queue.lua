-- Define the Queue table to hold all functions and data
local Queue = {}
Queue.__index = Queue  -- Set __index to refer to Queue for method lookup

--- Creates a new Queue instance.
---@return table
function Queue.new()
    -- Create a new table for the instance and set its metatable to Queue
    local self = setmetatable({}, Queue)

    self.line = {}

    return self

end

-- Enqueue method to add an item to the back of the queue
function Queue:enqueue(item)
    table.insert(self.line, item)
end

-- Dequeue method to remove and return the item at the front of the queue
function Queue:dequeue()
    if not self:is_empty() then
        return table.remove(self.line, 1)
    end
    return nil
end

-- Peek method to view the item at the front of the queue without removing it
function Queue:peek()
    if not self:is_empty() then
        return self.line[1]
    end
    return nil
end

-- Check if the queue is empty
function Queue:is_empty()
    return #self.line == 0
end

-- Get the size of the queue
function Queue:size()
    return #self.line
end

-- String representation for debugging purposes
function Queue:__tostring()
    local queue_str = "Queue: { "
    for _, item in ipairs(self.line) do
        queue_str = queue_str .. tostring(item) .. " "
    end
    return queue_str .. "}"
end

return Queue