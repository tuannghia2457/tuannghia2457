# Technology logo sources

These are authentic upstream logo assets used to identify technologies in the profile. Original artwork and colors are preserved. Product names and marks belong to their respective owners; displaying them indicates technology usage, not endorsement.

## Devicon

The following original SVGs come from [Devicon](https://github.com/devicons/devicon), pinned to commit [`7330accdbc47e2dc0c19789a48533c4a3c50fe58`](https://github.com/devicons/devicon/tree/7330accdbc47e2dc0c19789a48533c4a3c50fe58/icons):

Python, C++, TypeScript, JavaScript, Java, PyTorch, OpenCV, React, Next.js, Node.js, Express, PostgreSQL, Firebase, Git, Linux, Docker, and Playwright.

The upstream MIT license is included in [LICENSE-devicon.txt](./LICENSE-devicon.txt). All 17 SVGs have a `0 0 128 128` viewBox and contain vector artwork without external image dependencies.

## Primary project artwork

| File | Upstream source | Composition notes |
| --- | --- | --- |
| [ros.svg](./ros.svg) | [ROS artwork repository](https://github.com/ros-infrastructure/artwork/blob/4024191d62211c4d4fa024e9974dd372d92aa23a/ros_logo.svg) | Original ROS wordmark; viewBox `0 0 482.5625 127.625`. The shared ROS mark identifies ROS 2 in this profile. |
| [gazebo.svg](./gazebo.svg) | [Gazebo's own asset host](https://app.gazebosim.org/assets/images/gazebo_icon_white.svg) | Original white icon; dimensions `300 × 300`, no upstream viewBox. Use `0 0 300 300` when composing it. |
| [nav2.svg](./nav2.svg) | [Nav2 documentation repository](https://github.com/ros-navigation/docs.nav2.org/blob/76849a4062be342499889f4442838d6ecca77046/overrides/.icons/toggle/nav2-balloon-dark.svg) | Authentic dark-theme mark, viewBox `0 0 336.64001 427.51999`. Upstream artwork embeds a PNG data URI inside SVG; it is self-contained but is not pure vector. |

## Simple Icons

[mediapipe.svg](./mediapipe.svg) comes from [Simple Icons](https://github.com/simple-icons/simple-icons/blob/98820a4dc8c363ca72fa2c0d294ea4a0a9bba75d/icons/mediapipe.svg), pinned to commit `98820a4dc8c363ca72fa2c0d294ea4a0a9bba75d`. The upstream metadata identifies [Google's original MediaPipe icon](https://developers.google.com/static/mediapipe/images/mediapipe_icon.svg) as its source and `#0097A7` as the canonical brand color. That fill is applied to the otherwise unchanged monochrome vector silhouette. Its viewBox is `0 0 24 24`. The upstream CC0 license is included in [LICENSE-simple-icons.txt](./LICENSE-simple-icons.txt).

Exact source URLs, dimensions, and dependency checks are recorded in [sources.json](./sources.json).

No authentic standalone SVG brand mark was located for RViz in its primary source repository during this update. Its name can appear as text. SQL denotes a language rather than one product, so a database symbol is a semantic icon rather than a brand logo.

For panel composition, embed the SVG children and preserve their fills, gradients, and viewBox proportions. Namespace internal IDs and their references to avoid collisions. Express and Next.js contain black artwork; provide suitable local contrast without recoloring the logo.
