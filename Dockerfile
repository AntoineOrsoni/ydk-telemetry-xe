FROM ydkdev/ydk-py
COPY ./my_app /root/my_app/
WORKDIR /root/my_app/
RUN pip3 install -r requirements.txt
CMD python3 -i main.py