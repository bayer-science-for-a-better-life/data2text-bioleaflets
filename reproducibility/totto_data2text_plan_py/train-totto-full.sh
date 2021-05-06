BASE=~/ToTTo
IDENTIFIER=full
GPUID=0

python27 train.py -data $BASE/preprocess/totto-full -save_model $BASE/gen_model/$IDENTIFIER/totto -encoder_type1 mean -decoder_type1 pointer -enc_layers1 1 -dec_layers1 1 -encoder_type2 brnn -decoder_type2 rnn -enc_layers2 2 -dec_layers2 2 -batch_size 1 -feat_merge mlp -feat_vec_size 600 -word_vec_size 600 -rnn_size 600 -seed 1234 -start_checkpoint_at 4 -epochs 25 -optim adagrad -learning_rate 0.15 -adagrad_accumulator_init 0.1 -report_every 100 -copy_attn -truncated_decoder 100 -gpuid $GPUID -attn_hidden 64 -reuse_copy_attn -start_decay_at 4 -learning_rate_decay 0.97 -valid_batch_size 1
