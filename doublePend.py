import manim as M
from math import sin, cos, pi
import numpy as np
from numpy.linalg import inv


class DoublePendulum(M.Scene):
    def __init__(self, l2):
        # Masses of the ball
        self.m1 = 2
        self.m2 = 5
        # Length of the rigid massless rods
        self.l1 = 2
        self.l2 = l2
        # Acceleration due to gravity
        self.g = 9.81
        # Factor to decrease the velocity by
        self.dissipation_factor = 0.999999

        # timestep
        self.dt = 0.0001
        # runtime represents how long each frame should run. runtime = 1/fps
        # Change frame rate from here
        M.config.frame_rate = 60
        # do not change this
        self.runtime = 1 / M.config.frame_rate
        # time_max represents for how long (in seconds) the overall animation should run
        self.time_max = 10
        # Initial angles of the masses
        self.theta1, self.theta2 = (pi, pi / 2)
        # number of seconds before current time to show trail
        self.trail_seconds = 2.5

        super().__init__()

    def G(self, y, t):
        """
        Args:
            y ([list]): [Array representing the state of the system]
        """
        v1, v2 = y[0], y[1]
        a1, a2 = y[2], y[3]

        m11, m12 = (self.m1 + self.m2) * self.l1, self.m2 * self.l2 * cos(
            a1 - a2
        )
        m21, m22 = self.l1 * cos(a1 - a2), self.l2
        m = np.array([[m11, m12], [m21, m22]])

        f1 = -self.m2 * self.l2 * v2 * v2 * sin(a1 - a2) - (
            self.m1 + self.m2
        ) * self.g * sin(a1)
        f2 = self.l1 * v1 * v1 * sin(a1 - a2) - self.g * sin(a2)
        f = np.array([f1, f2])

        accel = inv(m).dot(f)

        return np.array([accel[0], accel[1], v1, v2])

    def RK4_step(self, y, t, dt):
        """Creates a step to update the state based on the time step

        Args:
            y ([list]): [Array representing the state of the system]
            dt ([float]): [Time step for RK4. Preferably very small for accuracy]

        Returns:
            [float]: [Returns to the value to update the state by]
        """
        k1 = self.G(y, t)
        k2 = self.G(y + 0.5 * k1 * dt, t + 0.5 * dt)
        k3 = self.G(y + 0.5 * k2 * dt, t + 0.5 * dt)
        k4 = self.G(y + k3 * dt, t + dt)

        return dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6

    def update(self, theta1, theta2):
        """Finds coordinates of the the two masses using their respective angles

        Args:
            theta1 ([float]): [angle of first mass]
            theta2 ([float]): [angle of second mass]

        Returns:
            [tuple of tuples]: [The inner tuples represent the coordinates of the masses]
        """
        x1 = self.l1 * sin(theta1)
        y1 = -self.l1 * cos(theta1)
        x2 = x1 + self.l2 * sin(theta2)
        y2 = y1 - self.l2 * cos(theta2)

        return (x1, y1), (x2, y2)

    def getline(self, Point1, Point2):
        """[Generates a line between the center of the given Circles which represent the masses]

        Args:
            Point1 ([Circle]): [Circle represent the first mass]
            Point2 ([Circle]): [Circle represent the second mass]

        Returns:
            [Line]: [Returns a line between the center of two masses]
        """
        start_point = Point1.get_center()
        end_point = Point2.get_center()
        line = M.Line(start_point, end_point).set_stroke(width=2)
        return line

    def construct(self):
        # Error checking of the times used
        if self.trail_seconds >= self.time_max:
            raise Exception(
                "Seconds of trail must be smaller than time of animation"
            )
        elif self.trail_seconds < self.runtime:
            raise Exception(
                "Seconds of trail must be greater than runtime of each frame"
            )

        # State-space form
        # y = [v1, v2, theta1, theta2]
        # Do not confuse this y variable for y coordinates
        y = np.array([0.0, 0.0, self.theta1, self.theta2])

        # Getting the positions of the ball at each time
        t_array = np.arange(0, self.time_max, self.dt)

        # Points is a 2 dimensional array. First and second rows contain
        # tuples representing the coordinates of the first and second ball
        # ,respectively, after every time step
        points = np.zeros((2, len(t_array)), tuple)
        for idx, t in enumerate(t_array):
            points[0][idx], points[1][idx] = self.update(y[2], y[3])
            y = y + self.RK4_step(y, t, self.dt)
            # Decreasing velocity to simulate energy dissipation
            y[0:2] = self.dissipation_factor * y[0:2]

        # Adding the axes
        # axes = M.NumberPlane().set_opacity(0.1)
        axes = M.NumberPlane(
            x_range=(-4, 4, 1),
            y_range=(-4, 4, 1)
        ).set_opacity(0.1)
        axes = axes.set_opacity(0.1)
        self.add(axes)

        # Pendulum Motion
        Center = M.Dot()
        x1_initial, y1_initial = points[0][0]
        x2_initial, y2_initial = points[1][0]

        # Circles representing the masses
        Circle1 = (
            M.Dot(radius=0.04 * self.m1, z_index=10)
            .move_to(x1_initial * M.RIGHT + y1_initial * M.UP)
            .set_color(M.BLUE)
        )
        Circle2 = (
            M.Dot(radius=0.04 * self.m2, z_index=10)
            .move_to(x2_initial * M.RIGHT + y2_initial * M.UP)
            .set_color(M.BLUE)
        )

        # Initializing the lines and adding update functions
        Line1 = self.getline(Center, Circle1)
        Line1.add_updater(
            lambda mob: mob.become(self.getline(Center, Circle1))
        )
        Line2 = self.getline(Circle1, Circle2)
        Line2.add_updater(
            lambda mob: mob.become(self.getline(Circle1, Circle2))
        )

        # Adding the lines, masses and center dot to the screen
        self.add(Line1, Line2, Center, Circle1, Circle2)
        traj = M.VGroup()

        # Arrays containing components of their respective coordinates at each time interval
        x1 = [points1[0] for points1 in points[0]]
        y1 = [points1[1] for points1 in points[0]]
        x2 = [points2[0] for points2 in points[1]]
        y2 = [points2[1] for points2 in points[1]]

        # Adding the index referenced by for loop here so it can be used by
        # the trajectory update function
        i = 0

        traj = M.VGroup()

        # Update function for the trajectory
        def traj_update(mob):
            step = int(self.runtime / self.dt)
            start_idx = max(i - int(self.trail_seconds / self.dt), 0)
            end_idx = i - step
            if end_idx > start_idx:
                # Adding the points history of trajectory
                traj_points = [
                    x2[num] * M.RIGHT + y2[num] * M.UP
                    for num in range(start_idx, end_idx, step)
                ]
                traj_points.append(Circle2.get_center())

                # Creating VGroup for the trajectory
                updated_traj = M.VGroup().set_points_smoothly(traj_points)
                updated_traj.set_stroke(color=M.BLUE, width=1)
                mob.become(updated_traj)

        traj.add_updater(traj_update)
        self.add(traj)

        # Animating the masses moving
        for i in range(0, points.shape[1], int(self.runtime / self.dt)):
            self.play(
                Circle1.animate.move_to(x1[i] * M.RIGHT + y1[i] * M.UP),
                Circle2.animate.move_to(x2[i] * M.RIGHT + y2[i] * M.UP),
                run_time=self.runtime,
                rate_func=M.linear,
            )
