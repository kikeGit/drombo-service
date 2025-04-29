from flask import Blueprint, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return jsonify({"message": "Hola desde Flask!"})


# get_transfers

# get_transfer (get one)

# post_transfer

# update_transfer

# delete_transfer

# get_routes (date) - return all routes scheduled for today

# get_routes - return all routes 


# postpone_route - TBD

# send_route_to_rigitech (BLOQUEADO POR FRANCO)


## CRONJOBS

# recalculate_routes - Every 5 minutes
# update_transfer_status - Once per day
# create_routin_transfers - Once per week 