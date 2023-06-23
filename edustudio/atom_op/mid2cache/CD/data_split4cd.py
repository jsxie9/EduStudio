from edustudio.utils.common import UnifyConfig
from ..common.base_mid2cache import BaseMid2Cache
from edustudio.datafmt.utils import SpliterUtil
from sklearn.model_selection import StratifiedKFold, KFold
from itertools import chain


class M2C_RandomDataSplit4CD(BaseMid2Cache):
    default_cfg = {
        'seed': 2023,
        "divide_scale_list": [7,1,2],
    }

    def __init__(self, m2c_cfg, n_folds, is_dataset_divided) -> None:
        super().__init__(m2c_cfg)
        self.n_folds = n_folds
        self.is_dataset_divided = is_dataset_divided

        assert is_dataset_divided is False

    def _check_params(self):
        super()._check_params()
        assert 2 <= len(self.m2c_cfg['divide_scale_list']) <= 3
        assert sum(self.m2c_cfg['divide_scale_list']) == 10

    @classmethod
    def from_cfg(cls, cfg: UnifyConfig):
        m2c_cfg = cfg.datafmt_cfg.get(cls.__name__)
        n_folds = cfg.datafmt_cfg.n_folds
        is_dataset_divided = cfg.datafmt_cfg.is_dataset_divided
        return cls(m2c_cfg, n_folds, is_dataset_divided)

    def process(self, **kwargs):
        df = kwargs['df']

        if self.n_folds == 1:
            assert kwargs.get("df_train", None) is None
            assert kwargs.get("df_valid", None) is None
            assert kwargs.get("df_test", None) is None
            df_train, df_valid, df_test = self.one_fold_split(df)
            kwargs['df_train_folds'] = [df_train]
            kwargs['df_valid_folds'] = [df_valid] if df_valid is not None else []
            kwargs['df_test_folds'] = [df_test]
        else:
            df_train_list, df_test_list = self.multi_fold_split(df)
            kwargs['df_train_folds'] = df_train_list
            kwargs['df_test_folds'] = df_test_list

        return kwargs

    def one_fold_split(self, df):
        return SpliterUtil.divide_data_df_one_fold(
            df, divide_scale_list=self.m2c_cfg['divide_scale_list'], seed=self.m2c_cfg['seed']
        )

    def multi_fold_split(self, df):
        skf = KFold(n_splits=int(self.n_folds), shuffle=True, random_state=self.m2c_cfg['seed'])
        splits = skf.split(df)

        train_list, test_list = [], []
        for train_index, test_index in splits:
            train_df = df.iloc[train_index].reset_index(drop=True)
            test_df = df.iloc[test_index].reset_index(drop=True)
            train_list.append(train_df)
            test_list.append(test_df)
        return train_list, test_list

    def set_dt_info(self, dt_info, **kwargs):
        if 'stu_id:token' in kwargs['df'].columns:
            dt_info['stu_count'] = int(kwargs['df']['stu_id:token'].max() + 1)
        if 'exer_id:token' in kwargs['df'].columns:
            dt_info['exer_count'] = int(kwargs['df']['exer_id:token'].max() + 1)
        if kwargs.get('df_exer', None) is not None:
            if 'cpt_seq:token_seq' in kwargs['df_exer']:
                dt_info['cpt_count'] = len(set(list(chain(*kwargs['df_exer']['cpt_seq:token_seq'].to_list()))))
