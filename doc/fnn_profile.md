## Profile  
### Parameters and Shapes
```python  
 ProfileOptionBuilder = tf.profiler.ProfileOptionBuilder
	param_stats = tf.profiler.profile(
	tf.get_default_graph(),
		options=ProfileOptionBuilder.trainable_variables_parameter())
```

The output is  

```
Profile:
node name | # parameters
_TFProfRoot (--/16.18k params)
  b1 (20, 20/20 params)
  b2 (15, 15/15 params)
  b3 (10, 10/10 params)
  w1 (784x20, 15.68k/15.68k params)
  w2 (20x15, 300/300 params)
  w3 (15x10, 150/150 params)
```

### FLOPs  
```python  
tf.profiler.profile(
    tf.get_default_graph(),
    options=tf.profiler.ProfileOptionBuilder.float_operation())
```

The output is  

```
Profile:
node name | # float_ops
_TFProfRoot (--/32.27k flops)
  random_uniform (15.68k/31.36k flops)
    random_uniform/mul (15.68k/15.68k flops)
    random_uniform/sub (1/1 flops)
  random_uniform_1 (300/601 flops)
    random_uniform_1/mul (300/300 flops)
    random_uniform_1/sub (1/1 flops)
  random_uniform_2 (150/301 flops)
    random_uniform_2/mul (150/150 flops)
    random_uniform_2/sub (1/1 flops)
  Adam/mul (1/1 flops)
  Adam/mul_1 (1/1 flops)
  gradients/Mean_grad/Maximum (1/1 flops)
  softmax_cross_entropy_with_logits_sg/Sub (1/1 flops)
  softmax_cross_entropy_with_logits_sg/Sub_1 (1/1 flops)
  softmax_cross_entropy_with_logits_sg/Sub_2 (1/1 flops)
  softmax_cross_entropy_with_logits_sg_1/Sub (1/1 flops)
  softmax_cross_entropy_with_logits_sg_1/Sub_1 (1/1 flops)
  softmax_cross_entropy_with_logits_sg_1/Sub_2 (1/1 flops)
  ```

### Time and Memory  
We need `run_metadata` to profile time and memory.  
Here is the way to collect the run metadata.  

```python  
run_metadata = tf.RunMetadata()
with tf.Session() as sess:
  _ = sess.run(train_op,
               options=tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE),
               run_metadata=run_metadata)
```
Then, we can profile it with parameter `run_meta`.  

```python  
tf.profiler.profile(
    tf.get_default_graph(),
    run_meta=run_metadata,
    cmd='op',
    options=tf.profiler.ProfileOptionBuilder.time_and_memory())
```

The output is  

```
Profile:
node name 		| requested bytes		| total execution time	|accelerator execution time	|cpu execution time
VariableV2		0B (0.00%, 0.00%),		451us (100.00%, 39.67%), 0us (0.00%, 0.00%), 		451us (100.00%, 39.67%)
Assign     		194.11KB (100.00%, 60.00%),	433us (60.33%, 38.08%),	0us (0.00%, 0.00%),		433us (60.33%, 38.08%)
random_uniform  64.52KB (40.00%, 19.94%),	200us (22.25%, 17.59%),	0us (0.00%, 0.00%),		200us (22.25%, 17.59%)
Const			2.19KB (20.06%, 0.68%),	29us (4.66%, 2.55%),	0us (0.00%, 0.00%),			29us (4.66%, 2.55%)
Mul  			0B (0.00%, 0.00%),		19us (2.11%, 1.67%),	0us (0.00%, 0.00%),			19us (2.11%, 1.67%)
Add 			0B (0.00%, 0.00%), 		3us (0.44%, 0.26%), 	0us (0.00%, 0.00%),  		3us (0.44%, 0.26%)
Fill			62.72KB (19.39%, 19.39%),	2us (0.18%, 0.18%),	0us (0.00%, 0.00%), 		2us (0.18%, 0.18%)
```

### Visualize  
```python
tf.profiler.profile(
	tf.get_default_graph(),
		run_meta=run_metadata,
		cmd='graph',
		options=tf.profiler.ProfileOptionBuilder(
			tf.profiler.ProfileOptionBuilder.time_and_memory())
			.with_step(0).with_timeline_output('./test.out')
			.build()
)
```
op view doesn't support timeline yet. Consider graph/scope/code view.
Open a Chrome Browser, type URL `chrome://tracing`, and load the json file.

