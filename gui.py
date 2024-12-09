import argparse
from nicegui import ui, Client

# Custom
from gui.callbacks import GUIState
import gui.error_pages


icon_image_b64 = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNTEiIGhlaWdodD0iNTEiIHZpZXdCb3g9IjAgMCA1MSA1MSIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4NCjxwYXRoIGQ9Ik01MSAyNS41QzUxIDM5LjU4MzMgMzkuNTgzMyA1MSAyNS41IDUxQzExLjQxNjcgNTEgMCAzOS41ODMzIDAgMjUuNUMwIDExLjQxNjcgMTEuNDE2NyAwIDI1LjUgMEMzOS41ODMzIDAgNTEgMTEuNDE2NyA1MSAyNS41WiIgZmlsbD0id2hpdGUiLz4NCjxwYXRoIGQ9Ik01MSAyNS41QzUxIDM5LjU4MzMgMzkuNTgzMyA1MSAyNS41IDUxQzExLjQxNjcgNTEgMCAzOS41ODMzIDAgMjUuNUMwIDExLjQxNjcgMTEuNDE2NyAwIDI1LjUgMEMzOS41ODMzIDAgNTEgMTEuNDE2NyA1MSAyNS41WiIgZmlsbD0iIzQwNTFFOCIvPg0KPHBhdGggZD0iTTI0Ljk4NjUgMTUuNzU3MkMyNy4zODM2IDE1LjQ2MDQgMjkuODEyMyAxNi4xNDk1IDMxLjczODIgMTcuNjkyNEMzMy42NjY1IDE5LjIzNzEgMzQuOTMyNSAyMS41MTI4IDM1LjIzODMgMjQuMDI1M0MzNS41NDQyIDI2LjUzOCAzNC44NjE3IDI5LjA1ODEgMzMuMzU4NCAzMS4wMzEyQzMxLjg1NjcgMzMuMDAyMSAyOS42NjIzIDM0LjI2NDIgMjcuMjY0OSAzNC41NjExTDIxLjIxNzEgMzUuMzEwMkMyMC4zNDQ5IDM1LjMxOTcgMTkuNDg0IDM1LjAyNTEgMTguNzc4MyAzNC40NTk4QzE4LjA2ODUgMzMuODkxMSAxNy41NiAzMy4wODMgMTcuMzQ5NCAzMi4xNjU0TDE2LjY0MDIgMjYuMzM5MkMxNi4zMzQzIDIzLjgyNjUgMTcuMDE2OCAyMS4zMDY0IDE4LjUyMDEgMTkuMzMzM0MyMC4wMjE3IDE3LjM2MjUgMjIuMjE2MiAxNi4xMDAzIDI0LjYxMzYgMTUuODAzNEwyNC45ODY1IDE1Ljc1NzJaIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjUiLz4NCjwvc3ZnPg=="

parser = argparse.ArgumentParser()
parser.add_argument(
    "--avatar-path",
    default="drippy/female_model",
    help="Body model path",
    type=str,
)
args = parser.parse_args()


@ui.page('/{avartar}')
async def index(client: Client, avartar: str = "female_model"):
    # Start the interface!
    # gui_st = GUIState(args.avatar_path)
    gui_st = GUIState(f"drippy/{avartar}")

    # Connection end
    # https://github.com/zauberzeug/nicegui/discussions/1379
    await client.disconnected()
    print('Closed connection ', gui_st.pattern_state.id, '. Deleting files...')
    gui_st.release()


if __name__ == '__main__':
    ui.run(
            host="0.0.0.0",
            reload=False,
            favicon=icon_image_b64,
            title='Drippy Demo - Garment configuration',
            show=False
        )
