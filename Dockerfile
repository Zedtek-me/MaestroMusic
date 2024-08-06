FROM python:3
WORKDIR /musicapp
COPY . /musicapp/
COPY ./start_app.sh /musicapp/start_app.sh
RUN sed -i 's/\r$//g' /musicapp/start_app.sh
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 7000
EXPOSE 9000
RUN chmod +x /musicapp/start_app.sh
ENTRYPOINT [ "bash", "/musicapp/start_app.sh" ]
