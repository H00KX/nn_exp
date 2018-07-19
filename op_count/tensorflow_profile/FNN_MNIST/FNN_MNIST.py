import tensorflow as tf

import mnist

class FNN:
	INPUT_SIZE = 28 * 28
	HIDDER1_SIZE = 20
	HIDDER2_SIZE = 15
	OUTPUT_SIZE = 10

	def __init__(self, train_dataset, test_dataset):
		self.train_iters = train_dataset.make_one_shot_iterator().get_next()
		self.test_iters = test_dataset.make_one_shot_iterator().get_next()

		self.w1 = tf.Variable(tf.random_uniform((self.INPUT_SIZE, self.HIDDER1_SIZE)), name='w1')
		self.b1 = tf.Variable(tf.zeros((self.HIDDER1_SIZE, )), name='b1')
		self.w2 = tf.Variable(tf.random_uniform((self.HIDDER1_SIZE, self.HIDDER2_SIZE)), name='w2')
		self.b2 = tf.Variable(tf.zeros((self.HIDDER2_SIZE, )), name='b2')
		self.w3 = tf.Variable(tf.random_uniform((self.HIDDER2_SIZE, self.OUTPUT_SIZE)), name='w3')
		self.b3 = tf.Variable(tf.zeros((self.OUTPUT_SIZE, )), name='b3')


	def network(self, iters):
		hidden1_layer = tf.add(tf.matmul(iters[0], self.w1), self.b1)
		hidden2_layer = tf.add(tf.matmul(hidden1_layer, self.w2), self.b2)
		logits = tf.add(tf.matmul(hidden2_layer, self.w3), self.b3)
		output = tf.nn.softmax(logits)
		loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(\
			logits=logits, labels=iters[1]))
		return output, loss_op


	def train(self):
		_, loss_op = self.network(self.train_iters)
		optimizer = tf.train.AdamOptimizer(learning_rate=0.01)
		train_op = optimizer.minimize(loss_op)

		return train_op, loss_op

	def test(self):
		output, _ = self.network(self.test_iters)
		correct_pred = tf.equal(tf.argmax(output, 1), tf.argmax(self.test_iters[1], 1))
		accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
		
		return accuracy


if __name__ == "__main__":
	train_dataset, train_size = mnist.create_mnist_dataset(128, 'train')
	test_dataset, test_size = mnist.create_mnist_dataset(1, 'val')

	my_fnn = FNN(train_dataset, test_dataset)
	train_op, loss_op = my_fnn.train()
	test_op = my_fnn.test()

	# writer = tf.summary.FileWriter("./tb_out",tf.get_default_graph())
	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())
		step = 0
		while True:
			step += 1
			try:
				sess.run(train_op)
				if step % 50 == 0:
					print("step %d: loss: %f" % (step, sess.run(loss_op)))
			except tf.errors.OutOfRangeError:
				break

		print("accuracy: %f" % sess.run(test_op))
	# writer.close()
