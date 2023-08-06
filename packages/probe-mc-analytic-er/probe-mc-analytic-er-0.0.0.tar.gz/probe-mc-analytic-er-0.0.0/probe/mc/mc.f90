module mc
 use ziggurat
 implicit none
 real(8), parameter :: PI_D=3.141592653589793238462643383279502884197D0

 contains
!******************************************************
!generates random number with normal distribution with
!parameters mi, sigma }
 real(8) function norm_rd(mu,sigma)
  implicit none
  real(8), intent(in) :: mu, sigma

  norm_rd=rnor( )*sigma+mu

 end function norm_rd


!******************************************************
 function collision(m,m_gas,vx,vy,vz,vxg,vyg,vzg)
  implicit none
  real(8),intent(in) :: m, m_gas ! particle mass
  real(8),intent(in) :: vx,vy,vz
  real(8),intent(in) :: vxg,vyg,vzg
  real(8) :: vtx,vty,vtz,gx,gy,gz,g,vr, &
             gcx,gcy,gcz,sinchi,coschi,fis,p
  real(8), parameter :: kb = 1.3806503D-23
  real(8), dimension(3) :: collision

  p=1.0D0/(m+m_gas)

  vtx=(m*vx+m_gas*vxg)   ! rychlost teziste 
  vty=(m*vy+m_gas*vyg)
  vtz=(m*vz+m_gas*vzg)

  gx=vx-vxg               ! vzajemna rychlost 
  gy=vy-vyg
  gz=vz-vzg

  g=sqrt(gx**2+gy**2+gz**2)

  coschi=2.0D0*uni()-1.0D0
  sinchi=sqrt(1.0D0-coschi**2)
  fis=2.0D0*pi_d*uni()
  vr=sqrt(gy**2+gz**2)

  gcx=gx*coschi+vr*sinchi*sin(fis)
  gcy=gy*coschi+sinchi*(g*gz*cos(fis)-gx*gy*sin(fis))/vr
  gcz=gz*coschi-sinchi*(g*gy*cos(fis)+gx*gz*sin(fis))/vr
  
  collision(1)=p*(vtx+m_gas*gcx)
  collision(2)=p*(vty+m_gas*gcy)
  collision(3)=p*(vtz+m_gas*gcz)

 end function collision

end module mc
