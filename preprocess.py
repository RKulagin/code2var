#!/usr/bin/python
import pickle
import random
from argparse import ArgumentParser


def parse_vocab(path, min_frequency=1):
    with open(path) as file:
        total_lines = 0
        word_to_freq = {}
        for line in file:
            line_ = line.split(" ")
            if len(line_) != 2 or int(line_[1]) < min_frequency:
                continue
            word_to_freq[line_[0]] = line_[1]
            total_lines += 1
    if total_lines == 0:
        Exception("Empty or incorrect file given. Path: " + path)
    return word_to_freq


def save_dictionaries(path_freq, target_freq, word_freq, output_filename):
    output_file_path = output_filename + ".c2v.dict"
    with open(output_file_path, "wb") as file:
        pickle.dump(target_freq, file)
        pickle.dump(word_freq, file)
        pickle.dump(path_freq, file)
        print("Frequency dictionaries saved to: " + output_filename + ".c2v.dict")


def process_file(file_path, data_file_role, dataset_name, word_to_count, path_to_count, max_contexts, out_file_path):
    with open(file_path, 'r') as file:
        with open(out_file_path + '.csv', 'w') as output:
            for line in file:
                contexts = line.rstrip('\n').split(" ")
                target, contexts = contexts[0], contexts[1:]
                if len(contexts) > max_contexts:
                    contexts = random.sample(contexts, max_contexts)
                empty_filler = " " * (max_contexts - len(contexts))
                output.write(target + " " + " ".join(contexts) + empty_filler + "\n")
    print("processed file + " + file_path)
    print("generated file + " + out_file_path + ".csv")


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--train_data_vec", dest="train_data_path_vec", required=True)
    parser.add_argument("--test_data_vec", dest="test_data_path_vec", required=True)
    parser.add_argument("--val_data_vec", dest="val_data_path_vec", required=True)
    parser.add_argument("--train_data_var", dest="train_data_path_var", required=True)
    parser.add_argument("--test_data_var", dest="test_data_path_var", required=True)
    parser.add_argument("--val_data_var", dest="val_data_path_var", required=True)
    parser.add_argument("--max_contexts", dest="max_contexts", default=200, required=False)
    parser.add_argument("--word_vocab_size", dest="word_vocab_size", default=1301136, required=False)
    parser.add_argument("--path_vocab_size", dest="path_vocab_size", default=911417, required=False)
    parser.add_argument("--target_vocab_size", dest="target_vocab_size", default=261245, required=False)
    parser.add_argument("--word_histogram", dest="word_histogram", metavar="FILE", required=True)
    parser.add_argument("--path_histogram", dest="path_histogram", metavar="FILE", required=True)
    parser.add_argument("--target_histogram", dest="target_histogram", metavar="FILE", required=True)
    parser.add_argument("--net", dest="net", required=True)
    parser.add_argument("--output_name", dest="output_name", metavar="FILE", required=True,
                        default='data')
    args = parser.parse_args()

    train_data_path_vec = args.train_data_path_vec
    test_data_path_vec = args.test_data_path_vec
    val_data_path_vec = args.val_data_path_vec
    train_data_path_var = args.train_data_path_var
    test_data_path_var = args.train_data_path_var
    val_data_path_var = args.val_data_path_var

    target_freq = parse_vocab(args.target_histogram)
    path_freq = parse_vocab(args.path_histogram)
    word_freq = parse_vocab(args.word_histogram)

    for data_path, data_role in zip([test_data_path_vec, val_data_path_vec, train_data_path_vec],
                                    ['test_vec', 'val_vec', 'train_vec', 'test_var', 'val_var', 'train_var']):
        process_file(file_path=data_path, data_file_role=data_role, dataset_name=args.output_name,
                     word_to_count=word_freq, path_to_count=path_freq,
                     max_contexts=int(args.max_contexts), out_file_path=args.output_name)

    save_dictionaries(target_freq=target_freq, path_freq=path_freq, word_freq=word_freq,
                      output_filename=args.output_name)