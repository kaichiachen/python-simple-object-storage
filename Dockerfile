FROM rackspacedot/python38
COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt
COPY . /home/distributed_obj_storage_system
WORKDIR /home/distributed_obj_storage_system
