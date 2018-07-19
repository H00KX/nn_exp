import tensorflow as tf
import numpy as np

# dataset = tf.data.Dataset.from_tensor_slices(np.random.random([4, 3]))
# dataset = dataset.batch(2)
# iterator = dataset.make_one_shot_iterator()
# X = iterator.get_next()


X = tf.placeholder(tf.float32, shape=(None, 3), name='X')
y = tf.constant([[1, 2, 3, 4],
                 [1, 2, 3, 4],
                 [1, 2, 3, 4]], dtype=tf.float32)
mul_op = tf.matmul(X, y)

if __name__ == "__main__":
    x = np.random.random([2, 3])

    tf.profiler.profile(
        tf.get_default_graph(),
        cmd='op',
        options=tf.profiler.ProfileOptionBuilder.float_operation())

    run_metadata = tf.RunMetadata()
    with tf.Session() as sess:
        print(sess.run(mul_op, feed_dict={X: x},
                       options=tf.RunOptions(
                           trace_level=tf.RunOptions.FULL_TRACE),
                       run_metadata=run_metadata))

    tf.profiler.profile(
        tf.get_default_graph(),
        cmd='op', run_meta=run_metadata,
        options=tf.profiler.ProfileOptionBuilder.float_operation())
