from .serial_cmd import SerialCmd


def run_scipt_in_pico(tty_name, op_name, op_args=None):
    ser = SerialCmd(tty_name)

    with open(f'src/snippets/{op_name}') as f:
        code_tty =  f.read()
    
    if op_args is not None:
        for k, v in op_args.items():
            code_tty= code_tty.replace("{{" + k + "}}", v)

    o = ser.send_code(code_tty)
    ser.close()
    return '\n'.join(o)

def write_script_to_flash(tty_name, src_filename, set_as_main=False):
    ser = SerialCmd(tty_name)

    dst_filename = src_filename.split('/')[-1]

    with open(src_filename) as f:
        code_tty =  f.read()

    with open("src/snippets/script_to_flash") as f:
        script_to_flash = f.read()
        
    script_to_flash = script_to_flash.replace("{{FILE_NAME}}", dst_filename)
    script_to_flash = script_to_flash.replace("{{SCRIPT_CONTENT}}", code_tty)
    script_to_flash = script_to_flash.replace("{{RENAME_TO_MAIN}}", str(set_as_main))

    o = ser.send_code(script_to_flash)
    ser.close()
    return '\n'.join(o)

    