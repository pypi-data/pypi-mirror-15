"""TTV.

Functions to make test, train, validate sets for datasets.

Usage:
  ttv <name> [--split=<ratio>] <corpora>...
  ttv -h | --help
  ttv --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  <name>        name of the ttv file (e.g. experiment.yaml)
  <corpora>     path to a directory containing resource files
  -s --split=<ratio>  ttv ratio (e.g. (10, 80, 10)) [default: (20, 60, 20)]

"""

import os
import yaml
import random
import posixpath
from docopt import docopt

DEFAULT_TTV_RATIO = (20, 60, 20)


def make_ttv_yaml(corpora, path_to_ttv_file, ttv_ratio=DEFAULT_TTV_RATIO, deterministic=False):
    """ Create a test, train, validation from the corpora given and saves it as a YAML filename.

        Each set will be subject independent, meaning that no one subject can have data in more than one
        set

    # Arguments;
        corpora: a list of the paths to corpora used (these have to be formatted accoring to notes.md)
        path_to_ttv_file: the path to where the YAML file be be saved
        ttv_ratio: a tuple (e.g. (1,4,4) of the relative sizoe of each set)
        deterministic: whether or not to shuffle the resources around when making the set.
    """
    dataset = get_dataset(corpora)
    data_sets = make_ttv(dataset, ttv_ratio=ttv_ratio, deterministic=deterministic)

    def get_for_ttv(key):
        return (
            data_sets['test'][key],
            data_sets['train'][key],
            data_sets['validation'][key]
        )

    test, train, validation = get_for_ttv('subjects')

    number_of_files_for_each_set = list(get_for_ttv('number_of_files'))

    number_of_subjects_for_each_set = [len(x) for x in get_for_ttv('subjects')]

    dict_for_yaml = {
        'split': number_of_files_for_each_set,
        'subject_split': number_of_subjects_for_each_set,
        "test": test,
        "train": train,
        "validation": validation
    }

    with open(path_to_ttv_file, 'w') as f:
        yaml.dump(dict_for_yaml, f, default_flow_style=False)


def make_ttv(dataset, ttv_ratio=DEFAULT_TTV_RATIO, deterministic=False, limit_per_set=None):
    """
    Return a dict of test,train,validation sets with information regarding the split (lists of paths to data).

    Currently only separates by subjectID.

    Prioitises having a diverse set than a well fitting set. This means that the
    'knapsacking' is done by subjects with the least videos first, so that each set can have
    as many different subjects in as possible. If shuffle is set to true, the set is shuffled, which means this property does not hold

    returns {
        'subjects': dict of subjectID -> [resource_paths]
        'number_of_files': number of files the set has
        'expected_size' : (ttv_ratio * number_of_resources) or the limit_per_set (if not None)
    }
    """
    sizes_and_ids = [(len(dataset[key]), key) for key in dataset]
    number_of_resources = sum([x[0] for x in sizes_and_ids])


    # Get the smallest first
    sizes_and_ids.sort()
    if not deterministic:
        random.shuffle(sizes_and_ids)

    # normalise ttv_ratio
    ttv_ratio = [float(x) / sum(ttv_ratio) for x in ttv_ratio]

    data_sets = {}

    for key, ratio in zip(['test', 'train', 'validation'], ttv_ratio):
        expected_size = min(limit_per_set * ratio, (ratio * number_of_resources)) \
            if limit_per_set is not None else (ratio * number_of_resources)

        data_sets[key] = {
            'subjects': {},
            'number_of_files': 0,
            'expected_size': expected_size
        }


    def get_filenames(subjects):
        print('getting filename for :', subjects)
        return sum(list(map(lambda x: dataset[x], subjects)), [])


    set_names = list(data_sets.keys())
    i = 0
    while len(sizes_and_ids) > 0:
        if limit_per_set is not None:
            # if all the sets have more than the limit
            if all(map(lambda x: x['number_of_files'] >= x['expected_size'], data_sets.values())):
                break
        i += 1
        s = data_sets[set_names[i % len(set_names)]]
        if s['number_of_files'] < s['expected_size']:
            size, subjectID = sizes_and_ids.pop(0)
            s['subjects'][subjectID] = dataset[subjectID]
            s['number_of_files'] += size


    return data_sets


def split_list(arr, proportion):
    split_index = int(len(arr) * proportion)
    return arr[:split_index], arr[split_index:]


def get_dataset(corpora):
    """
    Return a dictionary of subjectID -> [path_to_resource]. This assumes the filename is strictured "<subjectID>_<metadata>"
    """
    # TODO: make filter methods for the files

    def make_posix_path(dirpath, filename):
        dirpath = posixpath.sep.join(dirpath.split(os.sep))
        return posixpath.join(dirpath, filename)

    wav_files_in_corpora = filter(
        lambda x: x.endswith('.wav'),
        sum(
            [list(map(lambda x: make_posix_path(corpus, x), os.listdir(corpus))) for corpus in corpora],
            []
        ),
    )

    dataset = {}
    for wav_file in wav_files_in_corpora:
        subjectID = os.path.split(wav_file)[-1].split('.')[0].split('_')[0]

        if subjectID in dataset:
            dataset[subjectID].append(wav_file)
        else:
            dataset[subjectID] = [wav_file]

    return dataset

if __name__ == '__main__':
    arguments = docopt(__doc__, version='0.0.1')

    try:
        ratio = arguments.get('--split')[1:-1].split(',')
        ratio = tuple(map(float, ratio))
        assert len(ratio) == 3
    except Exception as e:
        raise e

    make_ttv_yaml(arguments.get('<corpora>'), arguments.get('<name>'))


# def to_array(ttv):
#     """Turn the ttv into one large array of resources, and return the starting indexes of each set along with it."""
#     test = sum(ttv['test'].values, [])
