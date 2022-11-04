FROM victusfate/linguist_requirements
ENV DEBIAN_FRONTEND noninteractive

WORKDIR /var/www/linguist
COPY . /var/www/linguist
RUN make clean
RUN make dependencies
RUN make application
EXPOSE 5000

ENV PYTHONPATH='/var/www/linguist/:$PYTHONPATH'

CMD ["/var/www/linguist/entrypoint.sh"]
# ENTRYPOINT ["/var/www/linguist/entrypoint.sh"]

