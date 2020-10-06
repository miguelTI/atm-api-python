from server import app
from router import Router

router = Router(app)
router.mount_routes()
