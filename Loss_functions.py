import torch
import numpy as np
import torch.nn.functional as F

def distance_L2(x1, y1, x2, y2):
    return torch.hypot(x2-x1, y2-y1)[0]

def P(a,b,X):
    '''
    a: float
    b: float
    X: (2,width,height)
    '''
    x,y = X.size()
    Sum = 0
    maxi = 0
    for i in range(x):
        for j in range(y):
            d = distance_L2(a,b,X[0,i,j],X[1,i,j])
            Sum += d
            maxi = max(d,maxi)
    return 1 - ( Sum / ( x * y * maxi))

def produce_quantized_bins(grid, x_scale, y_scale, Q):
    '''
    grid: (width, height)
    x_scale: float
    y_scale: float
    Q: int

    list (x_q, y_q)
    '''
    width, height = grid.shape
    L = []
    for i in range(width):
        for j in range(height):
            L.append((grid[i,j],i,j))
    L.sort(reverse=True)
    L = L[:Q]
    M = []
    for p,x,y in L:
        a = x * x_scale - 110
        b = y * y_scale - 110
        M.append((a,b))
    return M

_GAUSSIAN_KERNEL = torch.from_numpy(np.array([[0.109634, 0.111842, 0.109634],[0.111842, 0.114094, 0.111842],[0.109634, 0.111842, 0.109634]]))

def compute_Z(img, bins):
    '''
    img: (2, width, height)
    bins: (2, Q)

    (Q, width, height)
    '''
    _, width, height = img.shape
    _, Q = bins.shape
    Z = torch.zeros((Q, width, height))

    for i in range(width):
        for j in range(height):
            mini = 0
            min_q = 0
            a = img[0,i,j]
            b = img[1,i,j]
            for k in range(Q):
                d = distance_L2(a,b,bins[0,k],bins[1,k])
                if d < mini:
                    min_q = k
                    mini = d
            Z[min_q, i, j] = 1
    
    Z = F.conv2D(Z, _GAUSSIAN_KERNEL)
    return Z

def compute_p_tilde(Z):
    '''
    Z: (Q, width, height)

    (Q)
    '''
    _, width, height = Z.shape
    p = torch.zeros((Q,1))
    p = torch.sum(torch.sum(Z,dim=1),dim=2)
    p /= width * height
    return p

def compute_w(p,epsilon=0.5):
    '''
    p: (Q)
    epsilon: int

    (Q)
    '''
    Q = p.shape[0]
    w = torch.pow((1 - epsilon)*p + epsilon / Q,-1)
    div = w * p
    return w / div

def compute_loss(y_pred, Z_true, bins, w):
    '''
    y_pred: (2, width, height)
    Z_true: (Q, width, height)
    bins: (2,Q)
    w: (Q, width, height)

    float
    '''
    Z_pred = compute_Z(y_pred,bins)
    Z_pred = torch.log(Z_pred)
    R = torch.sum(Z_true * Z_pred, dim=0)
    q_star = torch.argmax(Z_true, dim=0)
    v = torch.gather(w, dim=0, q_star)
    return -torch.sum(v * R)
    


    
