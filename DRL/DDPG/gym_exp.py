import tensorflow as tf
import tflearn 

inputs = tflearn.input_data(shape=[None, 3])
action = tflearn.input_data(shape=[None, 1])
net = tflearn.fully_connected(inputs, 400)
net = tflearn.layers.normalization.batch_normalization(net)
net = tflearn.activations.relu(net)

# Add the action tensor in the 2nd hidden layer
# Use two temp layers to get the corresponding weights and biases
t1 = tflearn.fully_connected(net, 300)
t2 = tflearn.fully_connected(action, 300)

net = tflearn.activation(
    tf.matmul(net, t1.W) + tf.matmul(action, t2.W) + t2.b, activation='relu')

# linear layer connected to 1 output representing Q(s,a)
# Weights are init to Uniform[-3e-3, 3e-3]
w_init = tflearn.initializations.uniform(minval=-0.003, maxval=0.003)
out = tflearn.fully_connected(net, 1, weights_init=w_init)