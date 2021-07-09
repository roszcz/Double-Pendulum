import manim as M

from doublePend import DoublePendulum


def main():
    # Pixels
    resolution = 1080, 1080
    M.config['video_dir'] = 'media/'
    M.config['images_dir'] = 'media/'
    M.config['save_last_frame'] = True

    # NumberPlane units (2 * "radius")
    M.config['frame_width'] = 2 * 4
    M.config['frame_height'] = 2 * 4

    l2 = 1
    output_name = 'douple-p-l2-hd-2'
    M.config['output_file'] = output_name

    # Make each movie in different resultion
    M.config['pixel_width'] = resolution[0]
    M.config['pixel_height'] = resolution[1]
    scene = DoublePendulum(l2=l2)
    scene.render()
    print('Finished rendering for:', l2)
    print('==' * 40)
