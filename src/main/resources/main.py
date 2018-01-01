import random as rnd

class GraphSolver(object):

	def __init__(self, test):
		pass

class Node(object):
	def __init__(self, name):
		self.name = name
		self.childern = []
		self.parents = []
		self.childern_weigths = []
		self.parent_weigths = []
		self.num_childern = 0
		self.num_parents = 0

	def add_child(self, child, weigth, nodeCalled = False):
		self.childern.append(child)
		self.childern_weigths.append(weigth);
		self.num_childern += 1
		if not nodeCalled:
			child.add_parent(self, weigth, nodeCalled = True)
		return self
		
	def add_parent(self, parent, weigth, nodeCalled = False):
		self.parents.append(parent)
		self.num_parents += 1
		if not nodeCalled:
			parent.add_child(self, weigth, nodeCalled = True)
		return self
		
class Task(object):
	def __init__(self, name, force, normal):
		self.name = name
		self.force = force
		self.normal = normal
		self.depends = []
		
	def add_depend(self, dep):
		self.depends.append(dep)
		
	def __str__(self):
		s = ""
		sp = str(self.force) + '/' + str(self.normal)
		s += self.name +' (' + sp +') \t'
		if len(self.depends) == 0:
			s += '--'
			return s
		for dep in self.depends:
			s += dep.name + ' '
		return s
	def __repr__(self):
		return self.__str__()
		
class Test(object):
	def __init__(self, task_namespace = 'A', num_of_tasks = 10, force_avg = 4, normal_avg = 10, num_of_depends = [2, 4, 3, 1]):
		sum = 0
		for num in num_of_depends:
			sum += num
		if num_of_tasks != sum:
			raise Exception("Wrong number of tasks")
			
		self.tasks = []
		numt = 0
		k = 0
		for dep in num_of_depends:
			for i in range(num_of_depends[k]):
				lb = rnd.randint(force_avg-2, force_avg+2)
				ub = rnd.randint(normal_avg-4, normal_avg+4)
				ctask = Task(chr(ord(task_namespace) + numt), lb, ub)
				cn = k
				
				while cn > 0:
					ttask = self.tasks[rnd.randint(0, numt-1)]
					while ttask in ctask.depends:
						ttask = self.tasks[rnd.randint(0, numt-1)]
					ctask.add_depend(ttask)
					cn -= 1
				
				numt += 1
				ctask.depends.sort(key = lambda x: x.name)
				self.tasks.append(ctask)
			k += 1
		
	def __str__(self):
		s = ""
		for t in self.tasks:
			s += t.__str__() + '\n'
		return s
		
def main():
	t = Test()
	print(t)
	
#if __name__ == '__main__':
main()
	
