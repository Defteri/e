FROM python/html
WORKDIR /rer
COPY Tert /rer/
ENTRYPOINT [ "python","-py","html","css" ]