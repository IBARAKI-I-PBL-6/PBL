"""
ログ出力に関する設定

Notes
-----
- ログ出力をしたいファイル
    先頭に次の2行を入れる
    >>>from logging import getLogger
    >>>logger = getLogger(__name__)
    (この後、logger.info()などでログ出力ができます。)

- 実行元のファイル
    実行用の関数に次の2行を入れる
    >>>from src.logging_setting import set_logger
    >>>set_logger()

    (実行用の関数は`if __name__ == "main:"にすることを推奨します`)
"""

import logging.config
logger = logging.getLogger()


def set_logger():
    """
    ログ出力のセッティングを行う

    実行用の関数で最初に呼び出す
    """
    
    logging.config.fileConfig("logging.conf", disable_existing_loggers=False,
                              encoding="UTF-8")  # logging.confからログの表示設定を読み込む
