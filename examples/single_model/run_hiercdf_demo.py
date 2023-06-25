import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../")
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from edustudio.quickstart import run_edustudio

run_edustudio(
    dataset='JunyiExerAsCpt',
    cfg_file_name=None,
    traintpl_cfg_dict={
        'cls': 'CDInterTrainTPL',        
    },
    datatpl_cfg_dict={
        'cls': 'HierCDFDataTPL',
        'M2C_ReMapId': {
            'share_id_columns': [{'cpt_seq:token_seq', 'cpt_head:token', 'cpt_tail:token', 'exer_id:token'}],
        }
    },
    modeltpl_cfg_dict={
        'cls': 'HierCDF',
    },
    evaltpl_cfg_dict={
        'clses': ['BinaryClassificationEvalTPL'],
    }
)
