import ray

ray.init()
data = [1,2,3]
oid = ray.put(data)
# get current node ip
nodeinfo = ray.nodes()[0]['NodeManagerAddress']

# set 'node' resource
@ray.remote
def set_resource(resource_name, resource_capacity):
	#by default, on actor's local node
	ray.experimental.set_resource(resource_name,resource_capacity)

ray.get(set_resource.remote(nodeinfo, 1))

# example task
@ray.remote
def get_max(data):
	return max(data)

# run the task on specified node
result = ray.get(get_max.options(resources={nodeinfo:1}).remote(data))
assert(max(data)==result)