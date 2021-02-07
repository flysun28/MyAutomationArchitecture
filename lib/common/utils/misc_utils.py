# coding=utf-8


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


def to_iterable(item, type_: (list, tuple, set)):
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


def extend_to_longgest(seq):
    '''
    :param seq: 必须为嵌套序列
    1. 获取元素的最大长度max_len
    2. 将每个子列表扩展到max_len，策略：复制最后一个元素，直到补齐长度
    e.g. [(1,2), (3,4,5)] ---> [(1,2,2), (3,4,5)]
    '''
    max_len = max([len(subseq) for subseq in seq])
    for idx, subseq in enumerate(seq):
        subseq = to_iterable(subseq, list)
        cur_len = len(subseq)
        if cur_len < max_len:
            last_ele = subseq[-1]
            subseq += (max_len-cur_len)*[last_ele]
            seq[idx] = subseq
    return seq
    