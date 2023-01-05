ARG VERSION=3.9
FROM python:${VERSION}-slim as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies in /.venv
COPY ./django_project/Pipfile .
COPY ./django_project/Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv sync --system

FROM python-deps AS runtime

# Create and switch to a new user
RUN useradd appuser
RUN mkdir -p /home/workspace
WORKDIR /home/workspace
USER appuser

CMD ["/bin/bash"]
