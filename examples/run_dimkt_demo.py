import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from edustudio.quickstart import run_edustudio

run_edustudio(
    dataset='assist_1213',
    cfg_file_name=None,
    datafmt_cfg_dict={
        'cls': 'DIMKTDataTPL',
        'load_data_from': 'rawdata',
        'raw2mid_op': 'R2M_ASSIST_1213',
        'is_save_cache': False,
        'M2C_BuildSeqInterFeats': {
            'seed': 2023,
            'divide_by': 'stu',
            'window_size': 200,
            "divide_scale_list": [7,1,2],
            "extra_inter_feats": []
        }
    },
    trainfmt_cfg_dict={
        'cls': 'KTInterTrainFmt',
        'batch_size': 64,
        'eval_batch_size': 64
    },
    model_cfg_dict={
        'cls': 'DIMKT',
    },
    evalfmt_cfg_dict={
        'clses': ['BinaryClassificationEvalFmt'],
    }
)

