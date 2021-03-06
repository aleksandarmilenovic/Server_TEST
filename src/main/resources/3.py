import random as rnd
import sys

#-------------------------------------------------------#
#														#
#                   Input:								#
#						Test							#
#					Output:								#
#				Graph Solved							#
#														#
#-------------------------------------------------------#

class GraphSolver(object):

	def __init__(self, test):
		test.apply_dependancy_reduction()
		self.nodes = []
		self.edges = []
		self.test = test
		self.nodes_count = 1
		#origin
		self.start_node = Node(self.nodes_count)
		self.nodes.append(self.start_node)
		self.nodes_count += 1
		
		for task in test.tasks:
			if len(task.depends) > 0:
				break
			#independent tasks
			nd = Node(self.nodes_count)
			self.nodes_count += 1
			self.nodes.append(nd)
			self.edges.append(Edge(task, self.start_node, nd))
			task.used = True
			
		for task in test.tasks:
			if not task.used:
				if len(task.depends) == 1:
					#single depends
					nd = Node(self.nodes_count)
					self.nodes_count += 1
					self.nodes.append(nd)
					self.edges.append(Edge(task, task.depends[0].fin_node, nd))
					task.used = True
				else:
					#multidepends before edge set reduction
					snode = Node(self.nodes_count)
					self.nodes_count += 1
					enode = Node(self.nodes_count)
					self.nodes_count += 1
					self.nodes.append(snode)
					self.nodes.append(enode)
					self.edges.append(Edge(task, snode, enode))
					task.used = True
					#fictive tasks denoted by forced and normal length of 0 (zero)
					for dep in task.depends:
						self.edges.append(Edge(Task("Fictive", 0, 0), dep.fin_node, snode))
		
		#detect false positive fictive tasks and reduce edge set
		for node in self.nodes[:]:
			if len(node.childern) == 1 and node.childern[0].task.force == 0 and node.childern[0].task.normal == 0:
				node.childern[0].dst_node.remove_parent(node.childern[0])
				for parent in node.parents:
					parent.dst_node = node.childern[0].dst_node
					node.childern[0].dst_node.add_parent(parent)
				self.nodes.remove(node)
				self.edges.remove(node.childern[0])
		
		#terminal node
		
		
		
		
		
		
		
		
		#reduce from multigraph to graph
		for node in self.nodes:
			rm_edges = []
			for i in range(len(node.childern)-1):
				for j in range(i+1, len(node.childern)):
					if node.childern[i].src_node == node.childern[j].src_node and node.childern[i].dst_node == node.childern[j].dst_node:
						rm_edges.append(node.childern[j])
						nd = Node(self.nodes_count)
						self.nodes_count += 1
						self.nodes.append(nd)
						e = Edge(node.childern[j].task, node.childern[j].src_node, nd)
						e2 = Edge(Task("Fictive", 0, 0), nd, node.childern[j].dst_node)
						self.edges.append(e)
						self.edges.append(e2)
			
			#collapse and remove
			for ed in rm_edges:
				ed.collapse_self()
				self.edges.remove(ed)
				
		#reindex nodes
		i = 1
		q = []
		v = []
		q.append(self.nodes[0])
		v.append(self.nodes[0])
		while len(q) > 0:
			q[0].name = str(i)
			i += 1
			for e in q[0].childern:
				if e.dst_node not in v:
					q.append(e.dst_node)
					v.append(e.dst_node)
			q.remove(q[0])
		
		self.nodes.sort( key = lambda n: int(n.name))
		self.edges.sort( key = lambda e: int(e.dst_node.name))
		
		self.end_node = Node("fin")
		for j in range(10):
			#merge loose ends into a singularity point of the terminal node
			for node in self.nodes:
				if len(node.childern) == 0 and node != self.end_node:
					for parent in node.parents:
						parent.dst_node = self.end_node
						self.end_node.add_parent(parent)
					self.nodes.remove(node)
		self.nodes.append(self.end_node)
			
		
		
		#reindex nodes
		i = 1
		q = []
		v = []
		q.append(self.nodes[0])
		v.append(self.nodes[0])
		while len(q) > 0:
			q[0].name = str(i)
			i += 1
			for e in q[0].childern:
				if e.dst_node not in v:
					q.append(e.dst_node)
					v.append(e.dst_node)
			q.remove(q[0])
		
		self.nodes.sort( key = lambda n: int(n.name))
		self.edges.sort( key = lambda e: int(e.dst_node.name))
		
		#self.end_node.name = "fin"
		
		
		#calculate times
		#normal times
		
		#earliest (and precalc for latest)
		q = []
		q.append(self.nodes[0])
		while len(q) > 0:
			for edge in q[0].childern:
				child_node = edge.dst_node
				q.append(child_node)
				if child_node.e < q[0].e + edge.task.normal:
					child_node.e = q[0].e + edge.task.normal
					#child_node.l = q[0].e + edge.task.normal
					child_node.l = 9999999
			q.remove(q[0])
			
		#latest
		q = []
		q.append(self.end_node);
		self.end_node.l = self.end_node.e
		while len(q) > 0:
			for edge in q[0].parents:
				parent_node = edge.src_node
				#print("--")
				#print(parent_node) #debug
				#print(q[0])
				#print(edge)
				q.append(parent_node)
				if parent_node.l > q[0].l - edge.task.normal:
					parent_node.l = q[0].l - edge.task.normal
			q.remove(q[0])
			
		#time reserve
		for node in self.nodes:
			node.s = node.l - node.e
			
		self.edges.sort( key = lambda e: int(e.src_node.name))
		
				
		
	
	def __str__(self):
	
		s = ""
		s += "Nodes:\n"
		for node in self.nodes:
			s+= node.__str__() + " ";
		s += "\nEdges:\n"
		
		for edge in self.edges:
			s+= edge.__str__() + "\n"
		return s
	
	def show(self):
		pass
		
	def json_pack(self):
		pass
			
class Graph(object):
	def __init__(self):
		self.nodes = []
		self.edges = []

class Edge(object):
	def __init__(self, task, src_node, dst_node):
		self.task = task
		self.src_node = src_node
		self.dst_node = dst_node
		src_node.add_child(self)
		dst_node.add_parent(self)
		task.fin_node = dst_node
		
	def collapse_self(self):
		self.src_node.remove_child(self)
		#print(self)
		self.dst_node.remove_parent(self)
		
	def __str__(self):
		s = ""
		s += self.src_node.name + " -> " + self.dst_node.name +"  \t"
		s += self.task.subname()
		return s

class Node(object):
	def __init__(self, name):
		self.name = str(name)
		self.childern = []
		self.parents = []
		self.num_childern = 0
		self.num_parents = 0
		self.e = 0
		self.l = 0
		self.s = 0
		
	def __str__(self):
		s = ""
		s += "\nname: " + self.name
		s += "\nearliest: " + str(self.e)
		s += "\nlatest: " + str(self.l)
		s += "\nreserve:" + str(self.s)
		s += "\n"
		
		return s

	def add_child(self, edge):
		
		self.childern.append(edge)
		self.num_childern += 1
		
	def add_parent(self, edge):
		self.parents.append(edge)
		self.num_parents += 1
		
	def remove_parent(self, edge):
		self.parents.remove(edge)
		self.num_parents -= 1
		
	def remove_child(self, edge):
		self.childern.remove(edge)
		self.num_childern -= 1
		
		
		
class Task(object):
	def __init__(self, name, normal, force):
		self.name = name
		self.force = force
		self.normal = normal
		self.depends = []
		self.used = False
		self.fin_node = None
		
	def add_depend(self, dep):
		self.depends.append(dep)
		
	def subname(self):
		s = ""
		sp = str(self.force) + '/' + str(self.normal)
		s += self.name +' (' + sp +')'
		return s
		
	def __str__(self):
		s = ""
		sp = str(self.normal) + '/' + str(self.force)
		s += self.name +' (' + sp +') \t'
		if len(self.depends) == 0:
			s += '--'
			return s
		for dep in self.depends:
			s += dep.name + ' '
		return s
	def __repr__(self):
		return self.__str__()
		
	def find_dep(self, d):
		for dep in self.depends:
			if dep == d:
				return True
		for dep in self.depends:
			if dep.find_dep(d):
				return True
		return False
		
class Test(object):
	def __init__(self, task_namespace = 'A', num_of_tasks = 10, force_avg = 4, normal_avg = 10, num_of_depends = [2, 4, 3, 1], non_generated = False):
		
		self.tasks = []
		if non_generated:
			return
		sum = 0
		for num in num_of_depends:
			sum += num
		if num_of_tasks != sum:
			raise Exception("Wrong number of tasks")
			
		
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
	def add_task(self, task):
		self.tasks.append(task)
		
	def apply_dependancy_reduction(self):
		for t in self.tasks:
			for dep in t.depends[:]:
				for dep2 in t.depends[:]:
					if dep.find_dep(dep2):
						t.depends.remove(dep2)
		


def unit_test_case_3():
	t = Test(non_generated = True)
	A = Task('A', 10, 5)
	B = Task('B', 10, 9)
	C = Task('C', 2, 2)
	D = Task('D', 5, 4)
	E = Task('E', 1, 1)
	
	D.add_depend(A)
	D.add_depend(B)
	
	E.add_depend(A)
	E.add_depend(C)
	
	
	t.add_task(A)	
	t.add_task(B)	
	t.add_task(C)	
	t.add_task(D)	
	t.add_task(E)	
	
	
	return t		
		
def unit_test_case_2():
	t = Test(non_generated = True)
	A = Task('A', 10, 5)
	B = Task('B', 10, 9)
	C = Task('C', 2, 2)
	D = Task('D', 5, 4)
	E = Task('E', 1, 1)
	F = Task('F', 6, 3)
	G = Task('G', 3, 2)
	H = Task('H', 8, 4)
	I = Task('I', 2, 2)
	J = Task('J', 7, 4)
	K = Task('K', 7, 4)
	L = Task('L', 7, 4)
	M = Task('M', 7, 4)
	N = Task('N', 7, 4)
	
	B.add_depend(A)
	
	C.add_depend(A)
	
	D.add_depend(B)
	D.add_depend(C)
	
	E.add_depend(B)
	
	F.add_depend(B)
	
	G.add_depend(D)
	
	H.add_depend(D)
	
	I.add_depend(E)
	I.add_depend(F)
	
	J.add_depend(H)
	J.add_depend(I)
	
	K.add_depend(G)
	K.add_depend(J)
	
	L.add_depend(J)
	
	M.add_depend(L)
	
	N.add_depend(K)
	N.add_depend(M)
	
	t.add_task(A)	
	t.add_task(B)	
	t.add_task(C)	
	t.add_task(D)	
	t.add_task(E)	
	t.add_task(F)	
	t.add_task(G)	
	t.add_task(H)	
	t.add_task(I)	
	t.add_task(J)
	t.add_task(K)
	t.add_task(L)	
	t.add_task(M)	
	t.add_task(N)
	
	return t
	
def unit_test_case_1():
	t = Test(non_generated = True)
	A = Task('A', 10, 5)
	B = Task('B', 12, 9)
	
	C = Task('C', 2, 2)
	C.add_depend(A)
	
	D = Task('D', 5, 4)
	D.add_depend(A)
	
	E = Task('E', 1, 1)
	E.add_depend(B)
	
	F = Task('F', 6, 3)
	F.add_depend(B)
	
	G = Task('G', 3, 2)
	G.add_depend(C)
	
	H = Task('H', 8, 4)
	H.add_depend(D)
	
	I = Task('I', 2, 2)
	I.add_depend(F)
	
	J = Task('J', 7, 4)
	J.add_depend(G)
	J.add_depend(H)
	J.add_depend(I)
	
	t.add_task(A)	
	t.add_task(B)	
	t.add_task(C)	
	t.add_task(D)	
	t.add_task(E)	
	t.add_task(F)	
	t.add_task(G)	
	t.add_task(H)	
	t.add_task(I)	
	t.add_task(J)
	
	return t
	
		
def main():
	if len(sys.argv) != 2:
		raise Exception("Wrong number of arguments")
	s = sys.argv[1]
	'''
	s = "TEST\n"
	s += "14\n"
	s += "A 3 14 0\n"
	s += "B 4 7 0\n"
	s += "C 4 6 1 A\n"
	s += "D 3 9 1 C\n"
	s += "E 4 12 1 A\n"
	s += "F 4 7 1 B\n"				input sample
	s += "G 3 11 1 F\n"
	s += "H 5 9 1 E\n"
	s += "I 4 8 2 D G\n"
	s += "J 5 6 2 C I\n" 
	s += "K 5 11 2 G I\n"
	s += "L 4 10 2 E F\n"
	s += "M 6 6 3 B F K\n"
	s += "N 6 10 3 C F J\n"
	'''
	
	
	
	test_lines = s.split("\n")
	test_lines = test_lines[2:]
	t = Test(non_generated = True)
	for line in test_lines:
		sline = line.split(" ")
		if len(sline) < 3:
			continue
		print (sline)
		tsk = Task(sline[0], int(sline[1]), int(sline[2]))
		t.add_task(tsk)
		num = int(sline[3])
		for i in range(num):
			for ts in t.tasks:
				if ts.name == sline[4 + i]:
					tsk.add_depend(ts)
	#print(t)
	gs = GraphSolver(t)
	print("zadatak;")
	print(len(gs.nodes))
	for node in gs.nodes:
		print(node.name + " " + str(node.e) + " " + str(node.l) + " " + str(node.s))
	print(";")
	print(len(gs.edges))
	for edge in gs.edges:
		nm = edge.task.name if edge.task.force != 0 and edge.task.normal !=0 else "-1"
		print(edge.src_node.name + " " + edge.dst_node.name + " " + nm)
		
			
		
	
	
	
	
#if __name__ == '__main__':
main()
	
