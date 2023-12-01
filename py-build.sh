pyinstaller --noconfirm --log-level=WARN \
    --onefile \
    --hidden-import=requests \
    --hidden-import=backoff \
    --hidden-import=ratelimit \
    --upx-dir=/usr/local/share/ \
    --name="Talion Number Analyzer" \
    --icon="favicon.ico" \
    main.py