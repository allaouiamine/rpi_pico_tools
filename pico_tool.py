import argparse

from src import flash


def get_args():
    parser = argparse.ArgumentParser('Run python code in Raspberry Pi Pico or store a python file into the flash')
    parser.add_argument('-t', '--tty_name', action='store', help="tty_name for example /tty/ACM0", required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-l', '--list-files', action='store_true', help="list files in flash", default=False)
    group.add_argument('-r', '--read', action='store', help="read file from flah", default=False)
    group.add_argument('-d', '--delete', action='store', help="delete a file from flash" , default=None)
    group.add_argument('-D', '--delete-all', action='store_true', help="delete all files from flash", default=False)
    group.add_argument('-s', '--save', action='store', help="store a file in flash", default=None)
    parser.add_argument('-m', '--save-to-main', action='store_true', help="store a file in flash as main.py", default=False)
    args = parser.parse_args()
    if args.save_to_main and not args.save:
        parser.error('--save-to-main can only be used with --save')
    return args


def main():
    args = get_args()
    
    tty_name = args.tty_name

    if args.save:
        output = flash.write_script_to_flash(tty_name, args.save, set_as_main=args.save_to_main)
        print(output)
        return

    op_args = {}
    if args.list_files:
        op_name = 'list_files'

    elif args.read:
        op_name = 'read'
        op_args["FILE_NAME"] = args.read

    elif args.delete:
        op_name = 'delete'
        op_args["FILE_NAME"] = args.delete

    elif args.delete_all:
        op_name = 'delete_all'

    output = flash.run_scipt_in_pico(tty_name, op_name, op_args)
    return

if __name__ == "__main__":
    main()
