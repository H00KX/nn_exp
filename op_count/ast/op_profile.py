import ast
import astor
import numpy as np


class AddCounts(ast.NodeTransformer):
	def visit_BinOp(self, node):
		op_count_incr = self._count_increasement_each_time(node)
		for i in range(4):
			node.parent.parent.body.append(ast.AugAssign(\
				target=ast.Subscript(value=ast.Name(id='_count', ctx=ast.Load()), \
				slice=ast.Index(value=ast.Num(n=i)), ctx=ast.Store()),op=ast.Add(), \
				value=ast.Num(n=int(op_count_incr[i]))))

		return node

	def _count_increasement_each_time(self, node):
		count = np.array([0, 0, 0, 0])
		for i in ast.iter_child_nodes(node):
			if isinstance(i, ast.BinOp):
				count += self._count_increasement_each_time(i)
			if isinstance(i, ast.Add):
				count[0] += 1
			elif isinstance(i, ast.Sub):
				count[1] += 1
			elif isinstance(i, ast.Mult):
				count[2] += 1
			elif isinstance(i, ast.Div):
				count[3] += 1
		return count


class DeclGlobalCountForEachFunc(ast.NodeTransformer):
	def visit_FunctionDef(self, node):
		node.body.insert(0, ast.Global(names=['_count']))
		return node


def op_count(py_path):
	py_file = open(py_path, 'r')
	op_ast = ast.parse(py_file.read())
	# Add parent attribute to each node
	for node in ast.walk(op_ast):
		for child in ast.iter_child_nodes(node):
			child.parent = node

	print(astor.dump_tree(op_ast))
	# insert global _count list
	op_ast.body.insert(0, ast.Assign(targets=[ast.Name(id='_count', ctx=ast.Store())], \
		value=ast.List(elts=[ast.Num(n=0, ctx=ast.Store()), ast.Num(n=0, ctx=ast.Store()), \
			ast.Num(n=0, ctx=ast.Store()), ast.Num(n=0, ctx=ast.Store())], ctx=ast.Load())))
	
	# insert output function
	op_ast.body.append(ast.Expr(value=ast.Call(func=ast.Name(id='print', \
		ctx=ast.Load()), args=[ast.Name(id='_count', \
		ctx=ast.Load())], keywords=[])))
	AddCounts().visit(op_ast)
	DeclGlobalCountForEachFunc().visit(op_ast)
	ast.fix_missing_locations(op_ast)
	print(astor.dump_tree(op_ast))

	exec(compile(op_ast, filename="<ast>", mode="exec"))


if __name__ == "__main__":
	py_path = './test.py'
	op_count(py_path)