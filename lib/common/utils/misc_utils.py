# coding=utf-8
import re
import random
import string
import time
from functools import wraps


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            end = time.perf_counter()
            elapsed = round((end - start), 3)
            print('{} elapsed time: {}'.format(func.__qualname__, elapsed))
    return wrapper


def is_string(item)-> bool:
    return isinstance(item, str)


def is_sequence(seq)-> bool:
    if is_string(seq):
        return False
    try:
        iter(seq)
    except:
        return False
    return True


def to_iterable(item, type_:(list, tuple, set)):
    '''
    Convert the type of `item` to `type_`
    :param item: a sequence
    :param type_: a choice of [list, tuple, set]
    '''
    if is_sequence(item):
        return type_(item)
    else:
        raise ValueError(f'Argument {item} is not a sequence or a string.')
    

def to_iterable_nested(seq, ele_type:(list, tuple, set)=list):
    '''
    Recursively convert the type of each element to `ele_type`
    :param seq: a sequence
    :param ele_type: a choice of [list, tuple, set]
    '''
    assert is_sequence(seq)
    seq = to_iterable(seq, list)
    for idx, item in enumerate(seq):
        if is_sequence(item):
            seq[idx] = ele_type(item)
    return seq


def extend_to_longest(seq):
    '''
    :param seq: 必须为嵌套序列
    1. 获取元素的最大长度max_len
    2. 将每个子列表扩展到max_len，策略：复制最后一个元素，直到补齐长度
    e.g. [(1,2), (3,4,5)] ---> [(1,2,2), (3,4,5)]
    '''
    # 子元素不为序列，则强制转换为列表
    seq = [subseq if is_sequence(subseq) else [subseq] for subseq in seq]
    max_len = max([len(subseq) for subseq in seq])
    for idx, subseq in enumerate(seq):
        subseq = to_iterable(subseq, list)
        cur_len = len(subseq)
        if cur_len < max_len:
            last_ele = subseq[-1]
            subseq += (max_len-cur_len)*[last_ele]
            seq[idx] = subseq
    return seq


def ascii_to_chr_repr(str_with_ascii:str)-> str:
    str_with_chr = str_with_ascii
    imatches = re.finditer('%\w{2}', str_with_ascii)
    for m in imatches:
        raw = m.group()
        to_decimal = int(raw[1:], 16)
        str_with_chr = re.sub(raw, chr(to_decimal), str_with_chr)
    return str_with_chr


@timeit
def dictionary_should_contain_sub_dictionary(dict1:dict, dict2:dict):
    """
    Fails unless all items in `dict2` are found from `dict1`.
    """
    assert isinstance(dict1, dict), type(dict1)
    assert isinstance(dict2, dict), type(dict2)
    diffs = [k for k in dict2 if k not in dict1]
    missing_key_msg = "Following keys missing from first dictionary: %s" %', '.join(diffs)
    if diffs:
        raise AssertionError(missing_key_msg)
    diffs = ()
    for k2, v2 in dict2.items():
        v1 = dict1[k2]
        if k2 == 'payrequestid' and not v1.startswith(v2) or v1 != v2:
            diffs += 'Key "%s": %s != %s' %(k2, v2, v1),
    diff_value_msg = 'Following keys have different values:\n' + '\n'.join(diffs)
    print(diff_value_msg)
    if diffs:
        raise AssertionError(diff_value_msg)

    
def run_keyword_and_expect_error(err_key:str, keyword, *args, **kwargs):
    '''
    执行 keyword(*args, **kwargs)，期望报错，且报错信息中必须包含`err_key`
    :param err_key:
    :param keyword:
    '''
    if isinstance(keyword, str):
        keyword = eval(keyword)
    try:
        keyword(*args, **kwargs)
    except Exception as e:
        errmsg = ' '.join(e.args)
        if err_key in errmsg or err_key == '*':
            print('Expected error "%s" occurred, PASS!' %err_key)
        else:
            raise


def create_random_str(length:int):
    '''
    仅支持字母数字，长度小于等于62（26*2+10）
    '''
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


def get_letter_seqno(letter):
    '''
    sequence No is 1 based
    '''
    return string.ascii_uppercase.find(letter) + 1


def flatten_nested_dict(dictionary:dict):
    '''
    将嵌套字典的values更新到最外层
    '''
    res = {}
    for k, v in dictionary.items():
        if isinstance(v, dict):
            res.update(v)
        else:
            res[k] = v
    return res

