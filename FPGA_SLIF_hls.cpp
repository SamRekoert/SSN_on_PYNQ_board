void slif(int state_in, int counter_in, int in_c, int loops, int& spike, int& state_out, int& counter_out) {
	#pragma HLS INTERFACE ap_ctrl_none port=return
	#pragma HLS INTERFACE s_axilite port=state_in
	#pragma HLS INTERFACE s_axilite port=counter_in
	#pragma HLS INTERFACE s_axilite port=spike
	#pragma HLS INTERFACE s_axilite port=loops
	#pragma HLS INTERFACE s_axilite port=state_out
	#pragma HLS INTERFACE s_axilite port=counter_out
	#pragma HLS INTERFACE s_axilite port=in_c

	for (int i=0; i<=loops; i++) {
		switch (state_in) {
			case 0:
				if (1024 == counter_in) {
					state_out = 1;
					counter_out = 0;
				} else {
					state_out = state_in + 1;
				}
				break;
			case 1:
				if (1024 == counter_in) {
					spike = 1;
					state_out = 2;
					counter_out = 0;
				} else if (1 == in_c) {
					counter_out = counter_in + 1;
				} else if (counter_in != 0) {
					counter_out = counter_in - 1;
				}
				break;
			case 2:
				spike = 0;
				state_out = 0;
				break;
			default:
				spike = 0;
				state_out = 1;
				counter_out = 0;
		}
		state_in = state_out;
		counter_in = counter_out;
	}
}
