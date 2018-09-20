import logging
from argparse import ArgumentParser

import data_generator


def arg_parse():
    arg_p = ArgumentParser()
    arg_p.add_argument('--action', required=True)  # resample, tick_count, generate_plots
    arg_p.add_argument('--input_filename')

    # if action == resample
    arg_p.add_argument('--output_filename')
    arg_p.add_argument('--resample_frequency', default='5Min')

    # if action == generate_plots
    arg_p.add_argument('--use_quantiles', action='store_true')
    arg_p.add_argument('--output_dir')
    return arg_p


def main():
    args = arg_parse().parse_args()

    if args.action == 'resample':
        from utils import file_processor
        p = file_processor(args.input_filename, args.resample_frequency)
        if args.output_filename is not None:
            p.to_csv(args.output_filename)
        else:
            print(p)
    elif args.action == 'tick_count':
        from utils import count_ticks_per_day
        count_ticks_per_day(args.input_filename)
    elif args.action == 'generate_plots':
        data_gen_func = data_generator.generate_quantiles if args.use_quantiles else data_generator.generate_up_down
        print('Using: {}'.format(data_gen_func))
        data_gen_func(args.output_dir, args.input_filename)

    """
    assert len(args) == 4, 'Usage: python3 {} DATA_FOLDER_TO_STORE_GENERATED_DATASET ' \
                           'BITCOIN_MARKET_DATA_CSV_PATH USE_QUANTILES'.format(args[0])
    """


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    main()
