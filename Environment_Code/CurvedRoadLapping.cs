using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Lapping : MonoBehaviour
{
    public GameObject lap;

    public static int minuteCount;
    public static int secondsCount;
    public static float milliCount;
    public static string milliDisplay;

    public GameObject minuteBox;
    public GameObject secondsBox;
    public GameObject milliBox;

    void Update ()
    {
        milliCount += Time.deltaTime * 10;
        milliDisplay = milliCount.ToString("F0");
        milliBox.GetComponent<Text>().text = "" + milliDisplay;

        if (milliCount >= 10)
        {
            milliCount = 0;
            secondsCount += 1;
        }
        
        if (secondsCount <= 9)
        {
            secondsBox.GetComponent<Text>().text = "0" + secondsCount + ".";
        }
        
        else
        {
            secondsBox.GetComponent<Text>().text = secondsCount + ".";
        }

        if (secondsCount >= 60)
        {
            secondsCount = 0;
            minuteCount += 1;
        }

        if (minuteCount <= 9)
        {
            minuteBox.GetComponent<Text>().text = "0" + minuteCount + ":";
        }

        else 
        {
            minuteBox.GetComponent<Text>().text = minuteCount + ":";
        }
    }
    void OnTriggerEnter ()
    {
        
    }
}
