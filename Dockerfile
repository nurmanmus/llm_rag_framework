FROM python:3.10.13-slim-bookworm

# Set work directory
WORKDIR /app

# Install packages for virtual environment
RUN apt-get clean \
    && apt-get -y update \
    && apt -y update && apt -y upgrade \
    && apt-get install -y build-essential \
    && apt-get install -y python3-virtualenv \
    && apt-get install -y libgl1 libgl1-mesa-glx  libglib2.0-0 \
    && apt-get autoremove -y \
    && apt-get autoclean -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8


# core dependencies
COPY core/requirements/ /tmp/requirements

RUN pip install -U pip && \
    pip install -r /tmp/requirements/dev.txt

# service dependencies
COPY llm/requirements.txt /tmp/service_requirements.txt
RUN pip install -r /tmp/service_requirements.txt

RUN python3 -m spacy download en_core_web_sm

COPY . .
ENV PATH "$PATH:/core/scripts"

RUN useradd -m -d /app -s /bin/bash app \
    && chown -R app:app ./* && chmod +x ./core/scripts/*

USER app

CMD ["./core/scripts/start-dev.sh"]
