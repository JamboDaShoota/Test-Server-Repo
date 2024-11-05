local Q = require(script.Parent.Queue)

local text_q = Q.new()

text_q:enqueue("Jambo")
text_q:enqueue("is")
text_q:enqueue("the")
text_q:enqueue("best")

print(text_q:peek())


print(text_q:dequeue())

print(text_q:dequeue())

print(text_q:dequeue())

print(text_q:dequeue())

print(text_q:is_empty())
