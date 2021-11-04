#include <cmath>
#include <math.h>
#include <vector>

#include "jzq.h"
#include "imageio.h"

// library that enables threading with a thread-pool
#include "thread_pool.hpp"

#define FOR(A,X,Y) for(int Y=0;Y<A.height();Y++) for(int X=0;X<A.width();X++)

// fast approximation of exp -> See http://www.spfrnd.de/posts/2018-03-10-fast-exponential.html
template<typename Real, size_t degree, size_t i = 0>
    struct Recursion {
        static Real evaluate(Real x) {
            constexpr Real c = 1.0 / static_cast<Real>(1u << degree);
            x = Recursion<Real, degree, i + 1>::evaluate(x);
            return x * x;
        }
    };

template<typename Real, size_t degree>
    struct Recursion<Real, degree, degree> {
    static Real evaluate(Real x) {
        constexpr Real c = 1.0 / static_cast<Real>(1u << degree);
        x = 1.0 + c * x;
        return x;
    }
};

template<int N,typename T>
Vec<N,T> sampleBilinear(const Array2<Vec<N,T>>& I,const V2f& x)
{
  const int w = I.width();
  const int h = I.height();

  const int ix = std::floor(x(0));
  const int iy = std::floor(x(1));

  const float s = x(0)-ix;
  const float t = x(1)-iy;

  return Vec<N,T>((1.0f-s)*(1.0f-t)*Vec<N,float>(I(clamp(ix  ,0,w-1),clamp(iy  ,0,h-1)))+
                  (     s)*(1.0f-t)*Vec<N,float>(I(clamp(ix+1,0,w-1),clamp(iy  ,0,h-1)))+
                  (1.0f-s)*(     t)*Vec<N,float>(I(clamp(ix  ,0,w-1),clamp(iy+1,0,h-1)))+
                  (     s)*(     t)*Vec<N,float>(I(clamp(ix+1,0,w-1),clamp(iy+1,0,h-1))));
}

#include "thinks/poisson_disk_sampling/poisson_disk_sampling.h"

std::vector<V2f> genPts(const A2uc& M,float radius)
{
  namespace pds = thinks::poisson_disk_sampling;
  
  const auto x_min = std::array<float, 2>{{0.f,0.f}};
  const auto x_max = std::array<float, 2>{{float(M.width()-1),float(M.height()-1)}};
  const auto samples = pds::PoissonDiskSampling(radius, x_min, x_max);
  
  std::vector<V2f> O;
  for (const auto& sample : samples) {
    int x = sample[0];
    int y = sample[1];
    if (x>=0 && x<M.width() && y>=0 && y<M.height())
    {
      if (M(x,y)>64)
      {
        O.push_back(V2f(x,y));
      }
    }
  }
  
  return O;
}

const float SQR(float x) { return x*x; }

A2V2f readFlow(const std::string& fileName)
{
  A2V2f F = a2read<V2f>(fileName);
  if (F.empty()) { printf("error: failed to read flow %s\n",fileName.c_str()); exit(1); }
  return F;
}

void drawPts(A2V3f& O,const V2i& size,const std::vector<V2f>& Ps,const float sigma, const std::vector<V3f>& colors)
{  
    for(int i=0;i<Ps.size();i++)
    {
        const V2f p = Ps[i];
        const int r = 3*sigma;
        const float *color = colors[i].v;

        for (int y=p[1]-r;y<=p[1]+r;y++)
        for (int x=p[0]-r;x<=p[0]+r;x++)
        if (x>=0 && x<O.width() && y>=0 && y<O.height())
        {         
            const int width = O.size()[0];
            float *o_color = O.data()[x + y * width].v;

            // approxmiation of exp()
            // the range of the exponent for r = 3 * sigma is [-18, 0]
            // and thus a recursion level of 6 should suffice (which leads to maximum error of 2e-9)
            const float e_x = Recursion<float, 6>::evaluate(-(SQR(float(x)-p[0])+SQR(float(y)-p[1]))/(sigma*sigma));

            // use floating-point fma for a small improvement of lerp
            //O(x,y) = lerp(O(x,y),color, exponent);
            o_color[0] = fmaf(e_x, color[0], fmaf(-e_x, o_color[0], o_color[0]));
            o_color[1] = fmaf(e_x, color[1], fmaf(-e_x, o_color[1], o_color[1]));
            o_color[2] = fmaf(e_x, color[2], fmaf(-e_x, o_color[2], o_color[2]));
        }
  }
}

int main(int argc,char** argv)
{
  if (argc<11)
  {
    printf("%s mask\\%%03d.png flow-fwd\\%%03d.A2V2f flow-bwd\\%%03d.A2V2f firstframe lastframe numkeys key1 key2 ... keyN radius sigma output\\%%03d.png",argv[0]);
    return 1;
  }
  
  int argi=1;
  const char* maskFileFormat = argv[argi++];

  const char* flowFwdFormat = argv[argi++];
  const char* flowBwdFormat = argv[argi++];

  const int frameFirst = atoi(argv[argi++]);
  const int frameLast  = atoi(argv[argi++]);
  
  const int numKeys   = atoi(argv[argi++]);
  
  std::vector<int> keys;
  for(int i=0;i<numKeys;i++) { keys.push_back(atoi(argv[argi++])); }

  const float radius = atof(argv[argi++]);
  const float sigma  = atof(argv[argi++]);

  const char* outputFormat  = argv[argi++];

  printf("maskFileFormat: %s\n",maskFileFormat);  
  printf("flowFwdFormat:  %s\n",flowFwdFormat);
  printf("flowBwdFormat:  %s\n",flowBwdFormat);  
  printf("frameFirst:     %d\n",frameFirst);
  printf("frameLast:      %d\n",frameLast);
  printf("numKeys:        %d\n",numKeys);
  for(int i=0;i<numKeys;i++)
  {
    printf("keys[% 4d]:     %d\n",i,keys[i]);
  }
  printf("radius:         %.1f\n",radius);
  printf("sigma:          %.1f\n",sigma);
  printf("outputFormat:   %s\n",outputFormat);  

  Array2<std::vector<V2f>> pts(numKeys,frameLast+1);
  int max_pts_size = 0;

  V2i sizeO;

   // Thread-Pool for parallel applications
  thread_pool pool;
  std::vector<std::vector<V2f>> generated_points(keys.size());

  // generate points in parallel
  pool.parallelize_loop(
      0,
      keys.size() - 1,
      [&](const int a, const int b){
          for(int i=a; i<b; i++){
            const int frameKey = keys[i];
            const A2uc M = imread<unsigned char>(spf(maskFileFormat,frameKey).c_str());
            if (M.empty()) { printf("ERROR: failed to read mask %s\n",spf(maskFileFormat,frameKey).c_str());}  
            generated_points[i] = genPts(M, radius);
          }
      }
  );

  // Get size of video
  // assumes that masks and video frames have the same number of pixels
  sizeO = size(imread<unsigned char>(spf(maskFileFormat, keys[0]).c_str()));

  for(int k=0;k<keys.size();k++)
  {
    const int frameKey = keys[k];

    pts(k, frameKey) = generated_points[k];

    // keep track of max pts size to fill it later with colors
    max_pts_size = max_pts_size < generated_points[k].size() ? generated_points[k].size() : max_pts_size;

    pool.push_task([&](const int k, const int frameKey){
        if (frameLast>frameKey)
        {
            std::vector<V2f> Ps = generated_points[k];
            for(int frame=frameKey+1;frame<=frameLast;frame++)
            {
                const A2V2f F = a2read<V2f>(spf(flowBwdFormat, frame - 1));
                for(int i=0;i<Ps.size();i++) { Ps[i] = Ps[i] + sampleBilinear(F,Ps[i]); }      
                pts(k,frame) = Ps;
            }
    
        }
        if (frameFirst<frameKey)
        {
            std::vector<V2f> Ps = generated_points[k];
            for(int frame=frameKey-1;frame>=frameFirst;frame--)
            {
                const A2V2f F = a2read<V2f>(spf(flowFwdFormat, frame + 1));
                for(int i=0;i<Ps.size();i++) { Ps[i] = Ps[i] + sampleBilinear(F,Ps[i]); }      
                pts(k,frame) = Ps;
            }
        }
        },
        k,
        frameKey
    );
  }

  // create color scheme
  std::vector<V3f> colors;
  srand(420);
  for (size_t i = 0; i < max_pts_size; i++)
  {
      colors.push_back(V3f(rand()%255,rand()%255,rand()%255)/V3f(255,255,255));
  }

  // wait for computation of loops to finish
  pool.wait_for_tasks();

  // parallel drawing of images
  pool.parallelize_loop(
    frameFirst,
    frameLast + 1,
    [&](const size_t a, const size_t b){
        for(int frame=a; frame<b; frame++){
            A2V3f O(sizeO);
            fill(&O,V3f(0,0,0));

            for(int k=keys.size()-1;k>=0;k--)
            {
                drawPts(O,sizeO,pts(k,frame),sigma, colors);
            }
            imwrite(O,spf(outputFormat,frame));
        }
    }
  );
  
  return 1;
}
