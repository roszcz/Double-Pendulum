import manim as M

from doublePend import DoublePendulum


def main():
    resolution = 400, 400
    M.config['video_dir'] = 'media/'

    l2_values = [0.5 + 0.3 * it for it in range(5)]

    for it, l2 in enumerate(l2_values):
        output_name = f'douple-p-l2-{it}'
        M.config['output_file'] = output_name

        # Make each movie in different resultion
        M.config['pixel_width'] = resolution[0] + it * 100
        M.config['pixel_height'] = resolution[1] + it * 50
        scene = DoublePendulum(l2=l2)
        scene.render()
        print('Finished rendering for:', l2)
        print('==' * 40)
