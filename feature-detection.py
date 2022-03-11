import cv2

img = cv2.imread("./Images/1.png")
# img2 = cv2.imread("./Images/download.png")

cap = cv2.VideoCapture(0)

orb = cv2.ORB_create(10)
matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
kp = orb.detect(gray, None)
kp, des = orb.compute(gray, kp)

while True:
    ret, img2 = cap.read()

    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    kp2 = orb.detect(gray2, None)
    kp2, des2 = orb.compute(gray2, kp2)

    matches = matcher.match(des, des2, None)
    matches = sorted(matches, key= lambda x:x.distance)

    image = cv2.drawMatches(gray, kp, gray2, kp2, matches, None)
    cv2.imshow("match", image)

    # keypoints = cv2.drawKeypoints(gray, kp, None, color=(255,0,0), flags=cv2.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)
    # keypoints2 = cv2.drawKeypoints(gray2, kp2, None, color=(255,0,0), flags=cv2.DrawMatchesFlags_DRAW_RICH_KEYPOINTS)
    # cv2.imshow("image", keypoints), cv2.imshow("images", keypoints2)
    
    if cv2.waitKey(1) & 0xFF == ord("q"):
        cv2.destroyAllWindows()
        break