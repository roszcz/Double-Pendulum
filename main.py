import manim as M

from doublePend import DoublePendulum
from pendulum.scenes import main as pendulum_scenes


def main():
    # Pixels
    resolution = 100, 100
    M.config['video_dir'] = 'media/'
    M.config['images_dir'] = 'media/'
    M.config['save_last_frame'] = False

    # NumberPlane units (2 * "radius")
    M.config['frame_width'] = 2 * 4
    M.config['frame_height'] = 2 * 4

    l2 = 1
    output_name = 'douple-p-l2-hd-a'
    M.config['output_file'] = output_name

    # Make each movie in different resultion
    M.config['pixel_width'] = resolution[0]
    M.config['pixel_height'] = resolution[1]
    scene = DoublePendulum(l2=l2)
    scene.render()
    print('Finished rendering for:', l2)
    print('==' * 40)


def scene_from_trajectory(df):
    # Pixels
    resolution = 800, 800
    M.config['video_dir'] = 'media/'
    M.config['images_dir'] = 'media/'
    # M.config['save_last_frame'] = False

    # NumberPlane units (2 * "radius")
    M.config['frame_width'] = 2 * 4
    M.config['frame_height'] = 2 * 4

    output_name = 'cycle-search-0x06'
    M.config['output_file'] = output_name
    # M.config['save_as_gif'] = True
    # M.config['format'] = 'gif'
    M.config['format'] = None

    dt = 0.01
    l1 = 1.5
    l2 = 0.5
    # Make each movie in different resultion
    M.config['pixel_width'] = resolution[0]
    M.config['pixel_height'] = resolution[1]
    scene = pendulum_scenes.DoublePendulum(l1=l1, l2=l2, df=df, dt=dt)
    scene.render()
    print('Finished rendering for:', l2)
    print('==' * 40)
