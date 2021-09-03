import cv2
from math import atan, pi, fabs, sqrt, tan
import numpy as np

rect_width = 52
delta_dir = 10 * pi / 180


def get_dist_3d_p2p(color, center):
    return sqrt((color[0] - center[0]) ** 2 + (color[1] - center[1]) ** 2 + (color[2] - center[2]) ** 2)


def get_nearest_color(color_mean, color_center):
    nearest_dist = get_dist_3d_p2p(color_mean, color_center[0])
    nearest_color = 0
    for idx, center in enumerate(color_center[1:], 1):
        dist = get_dist_3d_p2p(color_mean, center)
        if dist < nearest_dist:
            nearest_dist = dist
            nearest_color = idx

    return nearest_color


def detect_color(ls_of_rects, color_center, img):
    '''
    '''
    # color_ls = ['red', 'green', 'blue', 'yellow', 'black']
    for idx, rect in enumerate(ls_of_rects):
        rect_img = img[rect[0][1] - 10:rect[0][1] + 10, rect[0][0] - 10:rect[0][0] + 10]
        # cv2.imshow("rect", rect_img)
        color_mean = rect_img.mean(axis=0).mean(axis=0).astype(int)
        color_id = get_nearest_color(color_mean, color_center)

        rect.append(color_id)
        #print(rect)


def is_between_2lines(points, lines):
    '''
    check if points are between 2 lines
    @param:
        points: coordination of points
            format: float [x, y]
        lines: formulars 'ax + by + c = 0' of 2 lines
            format: float [a, b, c]
    @return:
        boolean value
    '''
    for c in points:
        if (c[0] * lines[0][0] + c[1] * lines[0][1] + lines[0][2]) * (
                c[0] * lines[1][0] + c[1] * lines[1][1] + lines[1][2]) >= 0:
            return False

    return True


def get_intersection(line1, line2):
    '''
    find intersection's coordinate of line1 nad line2
    @param:
        lineX: a list contains center, direction and lenght of lineX
            format: [center, direction, lenght]
    @return:
        intersection's coordinate of line1 nad line2
            format: [x, y]
    '''
    a1, b1, c1 = get_fomular_of_line(line1)
    a2, b2, c2 = get_fomular_of_line(line2)
    if a1 == 0:
        y = (-c1 / b1)
        x = (-(y * b2 + c2) / a2)
    elif a2 == 0:
        y = (-c2 / b2)
        x = (-(y * b1 + c1) / a1)
    else:
        y = (c1 - c2) / (b2 - b1)
        x = (-(b1 * y + c1) / a1)
    # print('INter:',x, y)
    return x, y


def get_center_rect(rect, ls_of_cen_dir_len):
    '''
    find center's coordinate of rectangle
    @param:
        rect: a list contains pair of horizontal lines and pair of verticac lines
            format [[line_v1, line_v2], [line_h1, lin_h2]]
        ls_of_cen_dir_len: a  list contains center, direction and lenght of all lines
            format: [[center1, direction1, lenght1], [center2, direction2, lenght2], ...]
    @return: center's coordinate of rectangle
        format: int [x, y]
    '''
    ls_of_peaks = []
    for line_v in rect[0]:
        for line_h in rect[1]:
            inter = get_intersection(ls_of_cen_dir_len[line_v], ls_of_cen_dir_len[line_h])
            ls_of_peaks.append(inter)

    x_ = (ls_of_peaks[0][0] + ls_of_peaks[1][0] + ls_of_peaks[2][0] + ls_of_peaks[3][0]) / 4
    y_ = (ls_of_peaks[0][1] + ls_of_peaks[1][1] + ls_of_peaks[2][1] + ls_of_peaks[3][1]) / 4

    sum_direction = ls_of_cen_dir_len[rect[1][0]][1] + ls_of_cen_dir_len[rect[0][0]][1] + pi / 2
    sum_direction /= 2

    return (int(x_), int(y_)), sum_direction


def get_distance_p2p(p1, p2):
    '''
    calculate distance from point 'p1' to point 'p2'
    @param:
        pX: coordination of pX
            format: float
    '''
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def get_fomular_of_line(line):
    '''
    calculate formular of line
    @param:
        line: a list contains center, direction and lenght of line
            format: [center, direction, lenght]
    @return:
        formular of line 'ax + by +c = 0'
            format: float[a, b, c]
    '''
    if line[1] == 0:
        a = 0.0
        b = 1.0
    else:
        a = 1.0
        b = a * tan(line[1] + pi / 2)
    c = -(a * line[0][0] + b * line[0][1])
    return a, b, c


def get_distance_p2l(point, line):
    '''/
    calculate distance from point to line
    @param:
        point: coordination of the point
            format: [x, y]
        line: line's index in the list of all lines
            format: integer
    @ return: distance from point to line
        format: float
    '''
    a, b, c = get_fomular_of_line(line)

    return fabs(a * point[0] + b * point[1] + c) / sqrt(a ** 2 + b ** 2)


def get_distance_l2l(line1, line2):
    '''
    calculate distance from line1 to line2
    @param:
        lineX: a list contains center, direction and lenght of lineX
            format: [center, direction, lenght]
    @return:
        distance from line1 to line2
            format: float
    '''
    return (get_distance_p2l(line1[0], line2[:2]) + get_distance_p2l(line2[0], line1[:2])) / 2


def detect_pair_closed_parallel_lines(cluster, ls_of_cen_dir_len):
    '''
    find pairs of close parallel lines in cluster of lines
    @param:
        cluster: a list contains horizontal lines and vertical lines
            format: [[h1, h2, ...], [v1, v2, ...]]
        ls_of_cen_dir_len: a list contains center, direction, lenght of all lines
            format: float[[center, direction, lenght], ...]
    @return: a set contains list of couples vertical lines's index and a list os couples horizontal lines's index
        format:
    '''
    ls_of_couple_v = []
    for idx, i in enumerate(cluster[0]):
        for j in cluster[0][idx + 1:]:
            dist_l2l = get_distance_l2l(ls_of_cen_dir_len[i], ls_of_cen_dir_len[j])
            if dist_l2l >= rect_width * 0.15 and dist_l2l <= rect_width * 1.5:
                ls_of_couple_v.append((i, j))

    ls_of_couple_h = []
    for idx, i in enumerate(cluster[1]):
        for j in cluster[1][idx + 1:]:
            dist_l2l = get_distance_l2l(ls_of_cen_dir_len[i], ls_of_cen_dir_len[j])
            if dist_l2l >= rect_width * 0.15 and dist_l2l <= rect_width * 1.5:
                ls_of_couple_h.append((i, j))

    return (ls_of_couple_v, ls_of_couple_h)


def is_rect(v1, v2, h1, h2):
    '''
    check if for line v1, v2, h1, h2 are parts of real rect
    @param:
        v1, v2, h1, h2: lists contain center, direction and lenght of v1, v2, h1, h2
            format: float[center, direction, lenght]
    @return:
        boolean value
    '''
    line_v = (get_fomular_of_line(v1), get_fomular_of_line(v2))
    center_h = (h1[0], h2[0])

    line_h = (get_fomular_of_line(h1), get_fomular_of_line(h2))
    center_v = (v1[0], v2[0])

    if not is_between_2lines(center_h, line_v):
        return False
    elif not is_between_2lines(center_v, line_h):
        return False
    else:
        return True


def detect_real_rect(ls_of_cen_dir_len, clusters_of_paral_vert_lines):
    '''
    @param:
        ls_of_cen_dir_len: a list contains center, direction, lenght of all lines
            format: float[[center, direction, lenght], ...]
        clusters_of_paral_vert_lines: list of all clusters
            format: [[[h1, h2, ...], [v1, v2, ...]], ...]
    @return:
        ls_of_real_rects: a list contains center of real rects
            format: [[(x0, y0), dir0], [(x1, y1), dir1], ...]
    '''
    ls_of_center_rects = []
    ls_of_real_rects = []

    for cluster in clusters_of_paral_vert_lines:
        ls_of_pairs = detect_pair_closed_parallel_lines(cluster, ls_of_cen_dir_len)
        for v in ls_of_pairs[0]:
            for h in ls_of_pairs[1]:
                if is_rect(ls_of_cen_dir_len[v[0]], ls_of_cen_dir_len[v[1]],
                           ls_of_cen_dir_len[h[0]], ls_of_cen_dir_len[h[1]]):
                    # check if v and h are parts of a real rect
                    vh = [v, h]
                    # compute
                    center, direction = get_center_rect(vh, ls_of_cen_dir_len)

                    # cluster duplicated rects into groups
                    added = False
                    for i in ls_of_center_rects:
                        if get_distance_p2p(center, i[0][0]) < rect_width * 0.5:
                            i.append((center, direction))
                            added = True
                            break
                    if not added:
                        ls_of_center_rects.append([(center, direction)])

    # compute average center of duplicated rect group
    for c in ls_of_center_rects:
        x_sum = 0
        y_sum = 0
        dir_sum = 0
        for each in c:
            x_sum += each[0][0]
            y_sum += each[0][1]
            dir_sum += each[1]
        ls_of_real_rects.append([(int(x_sum / len(c)), int(y_sum / len(c))), dir_sum / len(c) / pi * 180])

    return ls_of_real_rects


def detect_rects(img, color_center):
    '''
    @return:
        ls_of_real_rects: a list contains center and directions of real rects
            format: [[(x0, y0), dir0], [(x1, y1), dir1], ...]
    '''
    # img = cv2.imread("photos/test11.png")
    # blur = cv2.GaussianBlur(img, (15, 15), 0) # loc nhieu
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    edged = cv2.Canny(blur, 20, 120)
    # cv2.imshow("blur", blur)
    # cv2.imshow("canny", edged)
    lines = cv2.HoughLinesP(edged, 1, np.pi / 180, 15, minLineLength=15, maxLineGap=5)
    ls_of_real_rects = []
    if lines is not None:
        # print("num of lines:", len(lines))
        clusters_of_paral_vert_lines, ls_of_cen_dir_len = find_clusters_of_paral_vert_lines(lines)
        # print("num of rects:", len(clusters_of_paral_vert_lines))
        ls_of_real_rects = detect_real_rect(ls_of_cen_dir_len, clusters_of_paral_vert_lines)
        detect_color(ls_of_real_rects, color_center, img)

        for idx, rect in enumerate(ls_of_real_rects):
            if rect[-1] == 4:
                ls_of_real_rects.pop(idx)

    return ls_of_real_rects


def get_center_direction_len(lines):
    '''
    calculate center, direction, lenght of all detected lines
    @param:
        ls_of_lines: list of all lines defined by 2 end-points
            format: [(x1, y1, x2, y2), (x1, y1, x2, y2), ...]
    @return:
        res: result
            format: [[center1, direction1, lenght1], [center2, direction2, lenght2], ...]
    '''
    res = list()

    for line in lines:
        x1, y1, x2, y2 = line[0]
        p1 = (x1, y1)
        p2 = (x2, y2)
        line_center = [(x1 + x2) // 2, (y1 + y2) // 2]
        lenght = get_distance_p2p(p1, p2)

        if x1 == x2:
            line_direction = pi / 2
        elif y1 == y2:
            line_direction = 0
        else:
            line_direction = atan((y1 - y2) / (x1 - x2))

        res.append([line_center, line_direction, lenght])

    return res


def find_in_neighbour(line, ls_of_cen_and_dir):
    '''
    find all lines which locate in neighbourhood around line
    @param:
        line: a list contains center, direction, lenght of line
            format: float[center, direction, lenght]
        ls_of_cen_and_dir: a list contains center, direction, lenght of all lines
            format: [[center0, direction0, lenght0], [center1, direction1, lenght1], ...]
    @return:
        list of horizontal lines and vertical lines
            format: [[h1, h2, ...], [v1, v2, ...]]
    '''
    center = line[0]
    direction = line[1]
    res = [[], []]

    for i, each in enumerate(ls_of_cen_and_dir):
        distance = get_distance_p2p(center, each[0])
        if distance < rect_width * 1.3 and distance >= rect_width * 0.3:
            if fabs(direction - each[1]) < delta_dir:
                res[0].append(i)
            elif fabs(fabs(direction - each[1]) - pi / 2) < delta_dir:
                res[1].append(i)
        elif distance < rect_width * 0.3:
            if fabs(direction - each[1]) < delta_dir:
                res[0].append(i)

    return res


def find_clusters_of_paral_vert_lines(lines):
    '''
    find the neighbours of each line in ls_of_lines
    @param:
        ls_of_lines: list of all lines defined by 2 end-points
            format: [(x1, y1, x2, y2), (x1, y1, x2, y2), ...]
    @return:
        clusters_of_paral_vert_lines: list of all clusters
            format: [[[h1, h2, ...], [v1, v2, ...]], ...]
        ls_of_cen_dir_len: a list contains center, direction, lenght of all lines
            format: float[[center, direction, lenght], ...]
    '''
    clusters_of_paral_vert_lines = list()
    ls_of_cen_dir_len = get_center_direction_len(lines)

    for line in ls_of_cen_dir_len:
        if line[2] > rect_width * 0.2:
            # if lenght of line is longer than rect_width*0.2
            clusters_of_paral_vert_lines.append(find_in_neighbour(line, ls_of_cen_dir_len))

    return clusters_of_paral_vert_lines, ls_of_cen_dir_len


def get_color_center():
    '''
    Tinh sample color cua 5 mau
    '''
    color_ls = ['red', 'green', 'blue', 'black']
    color_center = []
    for color in color_ls:
        img = cv2.imread('' + color + '.png')
        # tinh gia tri trung binh cua cac diem anh tren 3 thang mau RGB
        p = img.mean(axis=0).mean(axis=0).astype(int)
        # chuyen doi tu dinh dang numpy sang dinh dang list

        color_center.append(list(p))
    return color_center


color_center = get_color_center()

cap = cv2.VideoCapture(0)
# Setup tỉ lệ khung hình
cap.set(3, 640)
cap.set(4, 480)
cap.set(5, 30)
while True:

    img = cap.read()[1]

    # Cắt khung hình, chỉ lấy phần chứa băng chuyền

    # 160->320 => 160:260
    # Tìm tất cả các hình vuông trong khung hình bằng hàm detect_rects
    # ls_of_rects = [[[x, y], orientation, color],[], ...]
    ls_of_rects = detect_rects(img, color_center)
    # Thể hiện kết quả của việc xác định hình vuông trên cửa sổ origin
    color = [(255, 0, 255), (255, 0, 0), (0, 0, 255)]
    for rect in ls_of_rects:
        Minv = np.array([[0.0749, -0.0001, 0.7565],
                         [-0.0023, -0.0744, 18.8118],
                         [0.0000, 0.0001, 0.9756]])
        x = round(rect[0][0], 2)
        y = round(rect[0][1], 2)
        uv = np.array([[x], [y], [1]])
        realP = np.dot(Minv, uv)
        realPX = np.round(realP[0] / realP[2], 2) * 10
        realPY = np.round(realP[1] / realP[2], 2) * 10
        print(realPX)
        realPoints = np.array([[realPX], [realPY]])
        cv2.circle(img, rect[0], 2, color[0], thickness=1)
        cv2.putText(img, "{}  ".format(realPX) + "{}".format(realPY), ((rect[0][0]) - 40, (rect[0][1]) + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.circle(img, (img.shape[1] // 2, img.shape[0] // 2), 2, color[2],
               thickness=1)  # img.shape[0] is height ; img.shape[1] is width
    cv2.imshow('origin', img)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows()