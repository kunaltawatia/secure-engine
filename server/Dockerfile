FROM python

RUN python --version
RUN apt-get update && \
  apt install -y asciidoc libcap-dev libxml2-utils xsltproc docbook-xml docbook-xsl

WORKDIR /app
COPY . .

RUN cd iso && make && make install
RUN pip install -r requirements.txt

EXPOSE 5000
ENTRYPOINT [ "python" ]
CMD [ "server.py" ]