FROM python
WORKDIR /musicapp
COPY . /musicapp/
COPY ./start_app.sh /musicapp/start_app.sh
RUN sed sed -i 's/\r$//g' /start_app.sh
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 7000
EXPOSE 9000
ENTRYPOINT [ "bash", "-c", "/musicapp/start_app" ]
