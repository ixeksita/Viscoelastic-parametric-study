****************************************************************************************
**    SLS in its MAXWELL-ZENER FORM
**  UMAT, FOR ABAQUS/STANDARD INCORPORATING ELASTO-VISCOPLASTICITY WITH LINEAR-       **
**   VISCOELASTICITY AND AXI-SYMMETRIC ELEMENTS.                                      **
**   IMPLICIT INTEGRATION WITH INITIAL STIFFNESS JACOBIAN                             **
****************************************************************************************
****************************************************************************************
**
**
**
*USER SUBROUTINE
      SUBROUTINE UMAT(STRESS,STATEV,DDSDDE,SSE,SPD,SCD,
     1 RPL,DDSDDT,DRPLDE,DRPLDT,
     2 STRAN,DSTRAN,TIME,DTIME,TEMP,DTEMP,PREDEF,DPRED,CMNAME,
     3 NDI,NSHR,NTENS,NSTATV,PROPS,NPROPS,COORDS,DROT,PNEWDT,
     4 CELENT,DFGRD0,DFGRD1,NOEL,NPT,LAYER,KSPT,KSTEP,KINC)
C
      INCLUDE 'ABA_PARAM.INC'
C
      CHARACTER*80 CMNAME
C
C
      DIMENSION STRESS(NTENS),STATEV(NSTATV),
     1 DDSDDE(NTENS,NTENS),DDSDDT(NTENS),DRPLDE(NTENS),
     2 STRAN(NTENS),DSTRAN(NTENS),TIME(2),PREDEF(1),DPRED(1),
     3 PROPS(NPROPS),COORDS(3),DROT(3,3),DFGRD0(3,3),DFGRD1(3,3)
C
      REAL KE, GE, KMe, GMe, GV, KV, alpha
      REAL lambda1, lambda2, mu1, mu2, theta1, theta2
      REAL phi1, phi2, psi1, psi2
      REAL omega1, omega2, zeta1, zeta2
      REAL A, B, C, D, F, G, H
      REAL SIGsq, TrSIG, SIGterm
C
      REAL, DIMENSION(NTENS,NTENS):: DDSDE
      REAL, DIMENSION(NTENS,NTENS):: DDSDS
      REAL, DIMENSION(NTENS):: SIGold
C
C
C COEFFICIENTS
C
      KE = 175.44352890
      GE = 0.17544353
      KMe = 1252.724523
      GMe = 1.252725
      GV = 0.0662
C
C KV = infinite
      alpha = 0.0
C
        lambda1 = ( - GE/GV + 0.0 ) / 3.0
        lambda2 = ( - GE/GMe + KE/KMe ) / 3.0
        mu1 = GE/(2.0*GV)
	  mu2 = ( 1.0 + GE/GMe )/ 2.0
	  theta1 = 0.0
	  theta2 = - alpha*( 1.0 + KE/KMe )
	  phi1 = - 1.0/(6.0*GV) + 0.0
	  phi2 = - 1.0/(6.0*GMe) + 1.0/(9.0*KMe)
	  psi1 = 1/(4.0*GV)
	  psi2 = 1/(4.0*GMe)
	  omega1 = 0.0
	  omega2 = 1.0 + KE/KMe
	  zeta1 = 0.0
	  zeta2 = 1/(3.0*KMe)
C
	 A = lambda1*DTIME + lambda2
	 B = 2.0*mu1*DTIME + 2.0*mu2
	 C = theta1*DTIME + theta2
	 D = phi1*DTIME + phi2
	 F = 2.0*psi1*DTIME + 2.0*psi2
	 G = zeta1*DTIME + zeta2
	 H = omega1*DTIME + omega2
C
C CREATE JACOBIAN
C
C DEFINE TENSOR COEFFICIENTS RELATED TO NORMAL STRESSES
C
	     DO K1=1,NDI
	        DO K2=1,NDI
			 DDSDDE(K2,K1) = ( A - D*H/G )/F
			 DDSDE(K2,K1) = DTIME*( lambda1 - D*omega1/G )/F
			 DDSDS(K2,K1) = DTIME*( - phi1 + D*zeta1/G )/F
		    END DO
		   DDSDDE(K1,K1) = ( A + B - D*H/G )/F
		   DDSDE(K1,K1) = DTIME*( lambda1 + 2.0*mu1 - D*omega1/G )/F
		   DDSDS(K1,K1) = DTIME*( - phi1 - 2.0*psi1 + D*zeta1/G )/F
         END DO
C
C DEFINE TENSOR COEFFICIENTS RELATED TO SHEAR STRESSES
C
	     DO K1=NDI+1,NTENS
            DDSDDE(K1,K1) = B/(2.0*F)
            DDSDE(K1,K1) = DTIME*mu1/F
            DDSDS(K1,K1) = - 2.0*DTIME*psi1/F
         END DO
C
C STORE PRESENT STRESS STATE IN ARRAY SIGold
C
	     DO K1=1, NTENS
         SIGold(K1) = STRESS(K1)
	     END DO
C
C UPDATE STRESSES
C
		    DO K2=1,NTENS
				  DO K1=1,NTENS
					STRESS(K2) = STRESS(K2) + DDSDDE(K2,K1)*DSTRAN(K1)+
     1   		    DDSDE(K2,K1)*STRAN(K1)+
     2              DDSDS(K2,K1)*SIGold(K1)
					 END DO
			   END DO
C
      RETURN
      END