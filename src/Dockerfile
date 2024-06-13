FROM python:3.10

LABEL name="cgv-open-push"

WORKDIR /

COPY * .

# ntfy token e.g. "Bearer tk_abcdefghijklmnopqrstuvwxyz"
ENV NTFY_TOKEN=""
# private ntfy server address e.g. "https://ntfy.sh"
ENV PRIVATE_NTFY_SERVER_ADDRESS=""
# private ntfy prometheus address e.g. "https://ntfy.sh/metrics"
ENV PRIVATE_NTFY_PROMETHEUS_ADDRESS=""

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
CMD ["cgv_open_push_main.py"]

EXPOSE 5000