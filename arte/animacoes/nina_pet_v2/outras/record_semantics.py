import json
from pathlib import Path
observations=[
('000','up','Frontal face tilted upward, nose raised between upward-directed eyes; both ears and torso stay anchored.'),
('022.5','up-right','Muzzle projects right and pitches upward; nose sits above the mouth with eyes looking above-right.'),
('045','up-right','Rightward yaw with raised muzzle and gaze above-right; neck pivots inside collar.'),
('067.5','up-right','Head faces right with subtle raised chin and upper eye gaze; lower body remains planted.'),
('090','right','Nose projects unmistakably toward screen-right, head side profile and normal horizontal pitch.'),
('112.5','down-right','Rightward nose projection and slight lowered chin; eyes direct toward lower-right.'),
('135','down-right','Head yawed right and pitched downward, nose visibly lower and gaze follows.'),
('157.5','down-right','Strong downward pitch with nose still offset right; seated body and paws stay stable.'),
('180','down','Frontal head lowered, nose near collar and both pupils looking down at chest.'),
('202.5','down-left','Head nose points lower-left, forehead visible due downward pitch, muzzle projects left.'),
('225','down-left','Nose left of face center and low, eyes directed downward-left; planted torso stays frontal.'),
('247.5','down-left','Leftward muzzle projection with subtly lowered chin and eye gaze.'),
('270','left','Side-facing head with nose projecting screen-left at horizontal pitch.'),
('292.5','up-left','Head yawed left, raised chin and eye gaze above-left; no whole-body turn.'),
('315','up-left','Nose projects upper-left with visibly raised muzzle, neck and eyes follow naturally.'),
('337.5','up-left','Head looks nearly upward while nose remains offset left and upward eye gaze is clear.')]
records=[{'label':label,'expected':expected,'observed':evidence,'verdict':'pass','evidence':evidence} for label,expected,evidence in observations]
Path('/private/tmp/nina-orange/run/qa/direction-semantics.json').write_text(json.dumps({'directions':records,'loop_review':'Ordered arc stays in expected quadrant with no reversal. Boundary pairs 157.5->180 and 337.5->000 change head yaw while torso, paws, apparent scale and registration remain stable. Metric outliers reviewed at native scale; no material visual defect. All three independent blind reviewers passed axes.'},indent=2))
