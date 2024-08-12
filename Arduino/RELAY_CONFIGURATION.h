int RELAY_1 = 27;
int RELAY_2 = 29;
int RELAY_3 = 33;


//-----------------------------------------------------------------
//FUNCTION FOR OPERATING RELAY-------------------------------------
//-----------------------------------------------------------------
void operateRELAY(int RELAY, boolean OPENED) {
  if (OPENED)
    digitalWrite(RELAY, LOW);
  else
    digitalWrite(RELAY, HIGH);
}

//-----------------------------------------------------------------
//FUNCTION FOR SETTING RELAY PIN MODE------------------------------
//-----------------------------------------------------------------
void initRELAY(){
  pinMode(RELAY_1, OUTPUT);
  pinMode(RELAY_2, OUTPUT);
  pinMode(RELAY_3, OUTPUT);
  operateRELAY(RELAY_1, false);
  operateRELAY(RELAY_2, false);
  operateRELAY(RELAY_3, false);
}




