#!/usr/bin/env python3
# pip install coloredlogs verboselogs

import os
import coloredlogs
import logging
import verboselogs
import module

# logger = logging.getLogger(__name__)
logger = verboselogs.VerboseLogger(__name__)    # add logger.success

log_path = './hey/train.log'


def main():
    # logging.basicConfig(
    #     format="%(name)s: %(lineno)4d - %(levelname)s - %(message)s",
    #     level='INFO'
    #     )
    # coloredlogs.install(
    #     fmt='%(name)s: %(lineno)4d - %(levelname)s - %(message)s',
    #     level='INFO'
    #     )
    logger.debug('a')
    logger.info(__name__)
    logger.warning('bbb')
    logger.error('ccc')
    logger.success('Finished Training!')
    # a = 1 / 0
    logger.info(module.add(1., 2))

if __name__ == '__main__':
    """
    Initialise with NOTSET level and null device,
    and add stream handler separately.
    This way, the root logging level is NOTSET (log all),
    and we can customise each handler's behaviour.
    If we set the level during the initialisation,
    it will affect to ALL streams,so the file stream
    cannot be more verbose (lower level)
    than the console stream.
    """
    # logging.basicConfig(
    #     format='', level=logging.NOTSET, stream=open(os.devnull, 'w')
    #     )
    coloredlogs.install(
        fmt='%(name)s: %(lineno)4d - %(levelname)s - %(message)s',
        level=logging.NOTSET, stream=open(os.devnull, 'w')
        # 로그 메시지를 컬러로 출력
        # 모든 level 출력
        # 실제로는 로그 메시지를 /dev/null로 보내어 출력하지 않게 합니다.
        # 주로 테스트나 특정 환경에서 로그 출력을 억제하고자 할 때 사용될 수 있습니다.
        )

    # Different module different logging level
    # logging.getLogger('slowfast.utils.checkpoint').setLevel(logging.WARNING)

    console_handler = logging.StreamHandler()
    print(f"console_handler: {console_handler}")
    console_handler.setLevel(logging.INFO)
    console_format = coloredlogs.ColoredFormatter(
        '%(name)s: %(lineno)4d - %(levelname)s - %(message)s'
        # __main__:   26 - INFO - __main__
        )
    console_handler.setFormatter(console_format)

    # logging.getLogger('module').setLevel(logging.CRITICAL)
    f_handler = logging.FileHandler(log_path)
    print(f"f_handler: {f_handler}")
    f_handler.setLevel(logging.DEBUG)
    f_format = logging.Formatter(
        '%(asctime)s - %(name)s: %(lineno)4d - %(levelname)s - %(message)s'
        # 2024-05-26 13:54:22,309 - __main__:   25 - DEBUG - a
        )
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)
    root_logger.addHandler(f_handler)

    try:
        main()
    except Exception:
        logger.exception("Exception occurred")
